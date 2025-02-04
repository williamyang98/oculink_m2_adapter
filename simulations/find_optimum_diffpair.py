from collections import namedtuple
import argparse
import coloredlogs
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import shutil

logger = logging.getLogger(__name__)
# PCIe target differential impedance
Zd_0 = 85

def create_arg_parser():
    parser = argparse.ArgumentParser(
        prog="find_optimum_diffpair",
        description="Find the optimum differential pair from all simulated variants",
    )
    parser.add_argument("-i", "--input", dest="input", type=str, default="./variants_simulation")
    parser.add_argument("-o", "--output", dest="output", type=str, default="./variants_optimum_diffpair")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", "--debug", action="store_true", dest="debug")
    group.add_argument("-l", "--log", choices=["DEBUG", "INFO", "WARNING", "ERROR"], dest="log_level")
    return parser

def cleanup_param_name(name):
    # remove units
    name = re.sub(r"\(.*\)|\[.*\]", "", name)
    name = name.strip()
    # convert whitespace and underscores to dash
    name = re.sub(r"\s+|_", "-", name)
    name = name.lower()
    return name

Variant = namedtuple("Variant", ["name", "params"])
Result = namedtuple("Result", ["variant", "ports", "freq", "s11", "s21", "z"])

def str_to_complex(col):
    col = np.char.strip(col, '() ')
    col = np.char.replace(col, ' ', '')
    return col.astype(np.complex128)

def read_diffpair_result_from_dataframe(df, ports, variant):
    # convert to complex numbers
    for col_name in ("S11", "S21", "Zd (ohms)"):
        col = df[col_name].to_numpy().astype(str)
        col = str_to_complex(col)
        df[col_name] = col

    freq = df["Frequency (Hz)"].to_numpy() * 1e-9
    s11 = df["S11"].to_numpy()
    s21 = df["S21"].to_numpy()
    z = df["Zd (ohms)"].to_numpy()
    return Result(variant, ports, freq, s11, s21, z)

def main():
    parser = create_arg_parser()
    args = parser.parse_args()
    setup_logging(args)

    INPUT_DIR = os.path.realpath(args.input)
    VARIANT_FILE = os.path.join(INPUT_DIR, "variants.csv")
    VARIANT_DIR = os.path.join(INPUT_DIR, "variants")
    STATUS_FILE = os.path.join(INPUT_DIR, "status.txt")
    OUTPUT_DIR = os.path.realpath(args.output)

    with open(STATUS_FILE, "r") as fp:
        status = list(fp.readlines())
        status = [s.strip() for s in status]
        status = [s for s in status if len(s) > 0]
        status = set(status) 
    logger.info(f"Loaded {len(status)} statuses")

    df_variants = pd.read_csv(VARIANT_FILE)
    df_variants = df_variants.rename(columns=lambda x: x.strip())

    param_names = list(df_variants.columns)
    assert(param_names[0] == "Name")
    param_names = param_names[1:]
    assert(len(param_names) > 0)
    param_names = [cleanup_param_name(name) for name in param_names]
    logger.info(f"Optimising over {len(param_names)} parameters: [{','.join(param_names)}]")

    variants = []
    for row in df_variants.itertuples(index=False, name=None):
        name, params = row[0], row[1:]
        status_key = f"{name}_postprocess"
        if not status_key in status:
            logger.info(f"Variant {name} missing postprocessed results. Skipping...")
            continue
        variants.append(Variant(name, params))
    logger.info(f"Loaded {len(variants)} completed variants")

    diffpair_result_filename_regex = re.compile(r"diffpair_(\d)_(\d{4})\.csv")
    results = []
    for variant in variants:
        results_dir = os.path.join(VARIANT_DIR, variant.name, "results")
        results_filenames = os.listdir(results_dir)
        for filename in results_filenames:
            match = diffpair_result_filename_regex.match(filename)
            if match is None:
                continue
            excited_port_index = int(match[1])
            port_indices = [int(i) for i in match[2]]
            filepath = os.path.join(results_dir, filename)
            df = pd.read_csv(filepath)
            result = read_diffpair_result_from_dataframe(df, port_indices, variant)
            results.append(result)
    logger.info(f"Loaded {len(results)} diffpair results")

    create_dir(OUTPUT_DIR, cleanup=True)
    logger.info(f"Cleaned up output directory: {OUTPUT_DIR}")

    curr_results = results
    next_results = []
    total_params = len(param_names)
    for i in reversed(range(total_params)):
        fixed_param_names = param_names[:i]
        search_param_names = param_names[i:]
        logger.info(f"Optimising for fixed=[{','.join(fixed_param_names)}], search=[{','.join(search_param_names)}]")

        output_folder_name = fixed_param_names + [f"({name})" for name in search_param_names]
        output_folder_name = f"{'_'.join(output_folder_name)}"
        output_folder = os.path.join(OUTPUT_DIR, output_folder_name)
        create_dir(output_folder, cleanup=True)

        x_label = ':'.join(search_param_names)
        fixed_params_list = sorted(set(r.variant.params[:i] for r in curr_results))
        for fixed_params in fixed_params_list:
            search_results = [r for r in curr_results if r.variant.params[:i] == fixed_params]
            logger.info(
                f"Searching for fixed=[{','.join(map(str, fixed_params))}], "\
                f"search=[{','.join(map(str, search_param_names))}], "\
                f"total={len(search_results)}")
            search_params_list = [r.variant.params[i:] for r in search_results]
            x_ticks = [':'.join(map(str, search_params)) for search_params in search_params_list]
            title = \
                [f"{name}={value}" for name, value in zip(fixed_param_names, fixed_params)]+\
                [f"{name}=?" for name in search_param_names]
            title = ','.join(title)

            output_name = [f"{name}_{value}" for name, value in zip(fixed_param_names, fixed_params)] + search_param_names
            output_name = "_".join(output_name)
            fig, best_result = plot_reflectance_values(search_results, x_ticks, x_label, title)
            fig.savefig(os.path.join(output_folder, f"reflectance_{output_name}.png"))
            plt.close()
            fig = plot_s_parameters(search_results, x_ticks, x_label, title)
            fig.savefig(os.path.join(output_folder, f"s_params_{output_name}.png"), bbox_inches="tight")
            plt.close()

            logger.info(f"Found best result with search=[{','.join(map(str, best_result.variant.params[i:]))}]")
            next_results.append(best_result)

        curr_results = next_results
        next_results = []

    assert(len(curr_results) == 1)
    best_result = curr_results[0]
    x_ticks = [None]
    x_label = None
    title = ','.join([f"{name}={value}" for name, value in zip(param_names, best_result.variant.params)])
    output_name = "_".join([f"{name}_{value}" for name, value in zip(param_names, best_result.variant.params)])
    fig, _ = plot_reflectance_values([best_result], x_ticks, x_label, title)
    fig.savefig(os.path.join(OUTPUT_DIR, f"best_reflectance_{output_name}.png"))
    plt.close()
    fig = plot_s_parameters([best_result], x_ticks, x_label, title)
    fig.savefig(os.path.join(OUTPUT_DIR, f"best_s_params_{output_name}.png"), bbox_inches="tight")
    plt.close()

# this is the transformation used in Smith charts
def get_reflection_coefficient(Z, Z0):
    return (Z-Z0)/(Z+Z0)

def plot_reflectance_values(results, x_ticks, x_label, title):
    assert(len(results) == len(x_ticks))
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 4))
 
    R_list = [get_reflection_coefficient(r.z, Zd_0) for r in results]
    R_abs_list = [np.abs(R) for R in R_list]
    R_abs_mean_list = [np.mean(R) for R in R_abs_list]
    min_index, _ = min(enumerate(R_abs_mean_list), key=lambda x: x[1])
    min_result = results[min_index]

    # smith chart
    ax = axs[0]
    for x_tick, R in zip(x_ticks, R_list):
        ax.plot(np.real(R), np.imag(R), label=x_tick)
    ax.set_title(f"Smith chart")
    if x_label != None:
        ax.legend(title=x_label, loc="upper right")
    ax.grid(True, which="both")
    ax.set_xlabel("Re(Γ)")
    ax.set_ylabel("Im(Γ)")
    ax.axhline(0, color="black")
    ax.axvline(0, color="black")

    # violin plot of reflectance values
    ax = axs[1]
    ax.set_title(f"|Γ|")
    ax.violinplot(R_abs_list, showmeans=True, showmedians=False) 
    ax.set_xticks(np.arange(len(x_ticks))+1, labels=x_ticks)
    ax.grid(True, which="both")
    ax.set_xlabel(x_label)
    ax.set_ylabel("|Γ|")
    fig.suptitle(f"Reflectance ({title})")
    fig.tight_layout()
    return fig, min_result

def plot_s_parameters(results, x_ticks, x_label, title):
    assert(len(results) == len(x_ticks))
    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10, 6))

    for x_tick, result in zip(x_ticks, results):
        axs[0,0].plot(result.freq, 20*np.log10(np.abs(result.s11)), label=x_tick)
        axs[0,1].plot(result.freq, 20*np.log10(np.abs(result.s21)), label=x_tick)
        axs[1,0].plot(result.freq, np.unwrap(np.angle(result.s11))*(180/np.pi), label=x_tick)
        axs[1,1].plot(result.freq, np.unwrap(np.angle(result.s21))*(180/np.pi), label=x_tick)

    for ax_row in axs:
        for ax in ax_row:
            ax.grid(True, which="both")
 
    axs[0,0].set_ylabel("Magnitude (dB)")
    axs[1,0].set_ylabel("Angle (degrees)")
    axs[0,0].set_title("|S11|")
    axs[0,1].set_title("|S21|")
    axs[1,0].set_title("arg(S11)")
    axs[1,1].set_title("arg(S21)")
    axs[-1,0].set_xlabel("Frequency (GHz)")
    axs[-1,1].set_xlabel("Frequency (GHz)")
    if x_label != None:
        fig.legend(title=x_label, labels=x_ticks, bbox_to_anchor=(1.1, 0.75))
    fig.suptitle(f"S-params ({title})")
    fig.tight_layout()
    return fig

def create_dir(path, cleanup=False):
    directory_path = path
    if cleanup and os.path.exists(directory_path):
        shutil.rmtree(directory_path)
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)

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
