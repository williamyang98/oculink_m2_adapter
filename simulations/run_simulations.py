import argparse
import os
import logging
import csv
import coloredlogs
import subprocess

logger = logging.getLogger(__name__)

STATE_TRACKING_FILE = "status.txt"

def create_argument_parser():
    parser = argparse.ArgumentParser(
        prog="run_simulations",
        description="Run each simulation variant",
    )
    parser.add_argument("--config", dest="config", type=str, default="./simulation.json")
    parser.add_argument("-g", "--geometry", dest="geometry", action="store_true", help="Run geometry pass")
    parser.add_argument("-s", "--simulate", dest="simulate", action="store_true", help="Run simulation pass")
    parser.add_argument("-p", "--postprocess", dest="postprocess", action="store_true", help="Run postprocessing pass")
    parser.add_argument("-a", "--all", dest="all", action="store_true", help="Run all steps")
    parser.add_argument("-i", "--input", dest="input", type=str, default="./fab")
    parser.add_argument("-o", "--output", dest="output", type=str, default="./variants_simulation")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", "--debug", action="store_true", dest="debug")
    group.add_argument("-l", "--log", choices=["DEBUG", "INFO", "WARNING", "ERROR"], dest="log_level")
    parser.add_argument("-t", "--threads", dest="threads", type=int, default=None, help="Total threads to use for openEMS simulation")
    parser.add_argument("-r", "--restart", dest="restart", action="store_true", help="Restart all variant simulations")
    parser.add_argument("--ef", "--export-field", dest="export_field", action="store_true", help="Export E-field data from simulation")
    return parser

"""
Format of the output folder must be
- variants.csv: Stores csv list of (name, ....)
- variants/{name}: Folder for each variant of the simulation
- status.txt: Stores the currently completed steps for each variant as a list of strings
"""

def main():
    parser = create_argument_parser()
    args = parser.parse_args()
    setup_logging(args)

    variants = []
    with open(os.path.join(args.output, "variants.csv"), "r") as fp:
        reader = csv.reader(fp, delimiter=",", skipinitialspace=True)
        next(reader)
        for row in reader:
            variants.append(row[0])
    logger.info(f"Loaded {len(variants)} variants")

    state_tracker_filepath = os.path.join(args.output, STATE_TRACKING_FILE)
    state_tracker = set([])
    if args.restart:
        try:
            os.remove(state_tracker_filepath)
        except Exception as ex:
            logger.warning(f"Failed to remove old state tracker file when restarting: {ex}")
    else:
        try:
            with open(state_tracker_filepath, "r") as fp:
                for line in fp:
                    line = line.strip()
                    if len(line) > 0:
                        state_tracker.add(line)
            logger.info(f"Loaded {len(state_tracker)} tracked states")
        except Exception as ex:
            logger.warning(f"Failed to load state tracking file: {ex}")

    base_command_args = [
        "gerber2ems",
        "--config", args.config,
        "-i", args.input,
    ]
    if args.debug:
        base_command_args.append("--debug")
    if args.threads:
        base_command_args.extend(["--threads", str(args.threads)])
    if args.export_field:
        base_command_args.append("--export-field")

    def create_command_args(variant_dir, flags):
        command_args = []
        command_args.extend(base_command_args)
        command_args.extend(["--output", variant_dir])
        command_args.extend(flags)
        return command_args

    steps = [
        ("geometry", ["--geometry"], args.geometry or args.all),
        ("simulate", ["--simulate"], args.simulate or args.all),
        ("postprocess", ["--postprocess", "--render"], args.postprocess or args.all),
    ]

    with open(state_tracker_filepath, "a") as fp:
        for variant in variants:
            variant_dir = os.path.join(args.output, "variants", variant)
            variant_dir = os.path.realpath(variant_dir)
            for (name, flags, is_run) in steps:
                if not is_run:
                    logger.info(f"Skipping variant={variant}, step={name}")
                    continue
                action_key = "_".join((variant, name))
                if not action_key in state_tracker:
                    command_args = create_command_args(variant_dir, flags) 
                    retry_run(command_args)
                    fp.write(action_key + "\n")
                    fp.flush()
                    state_tracker.add(action_key)
                else:
                    logger.info(f"Cached variant={variant}, step={name}")

def retry_run(args, max_retries=5):
    logger.info(f"Running command={' '.join(args)}, max_retries={max_retries}")
    for i in range(max_retries):
        result = subprocess.run(args, capture_output=False)
        if result.returncode == 0:
            return
        logger.error(f"Failed to run {i+1}/{max_retries} with: code={result.returncode} command={' '.join(args)}")
    raise Exception(f"Command failed maximum retries: {max_retries}")

def setup_logging(args):
    level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    if args.log_level is not None:
        level = logging.getLevelName(args.log_level)

    if level == logging.DEBUG:
        coloredlogs.install(
            fmt="[%(asctime)s][%(name)s:%(lineno)d][%(levelname).4s] %(message)s",
            datefmt="%H:%M:%S",
            level=level,
            logger=logger,
        )
    else:
        coloredlogs.install(
            fmt="[%(asctime)s][%(levelname).4s] %(message)s",
            datefmt="%H:%M:%S",
            level=level,
            logger=logger,
        )

    # Temporary fix to disable logging from other libraries
    to_disable = ["PIL", "matplotlib"]
    for name in to_disable:
        disabled_logger = logging.getLogger(name)
        disabled_logger.setLevel(logging.ERROR)

if __name__ == "__main__":
    main()
