from gerber2ems.config import Config
from gerber2ems.constants import PIXEL_SIZE_MICRONS
from gerber2ems.simulation import Simulation
import gerber2ems.importer as importer
import PIL
import PIL.Image
import PIL.ImageChops
import PIL.ImageDraw
import PIL.ImageOps
import argparse
import coloredlogs
import json
import logging
import math
import numpy as np
import os
import shutil

logger = logging.getLogger(__name__)

COPLANAR_GAP_UM = 150

class HatchConfig:
    def __init__(self, width, gap, coplanar):
        self.width_um = width
        self.gap_um = gap
        self.coplanar_um = coplanar

def create_arg_parser():
    parser = argparse.ArgumentParser(
        prog="generate_hatch",
        description="Generate modified simulation files with varying hatch ground configurations",
    )
    parser.add_argument("--config", dest="config", type=str, default="./simulation.json")
    parser.add_argument("-i", "--input", dest="input", type=str, default="./fab")
    parser.add_argument("-o", "--output", dest="output", type=str, default="./output")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", "--debug", action="store_true", dest="debug")
    group.add_argument("-l", "--log", choices=["DEBUG", "INFO", "WARNING", "ERROR"], dest="log_level")
    parser.add_argument("--skip-convert", dest="skip_convert", action="store_true", help="Skip generating base Gerber images")
    parser.add_argument("--skip-cleanup", dest="skip_cleanup", action="store_true", help="Skip cleaning up old variants")
    return parser

def main():
    parser = create_arg_parser()
    args = parser.parse_args()
    setup_logging(args)

    OUTPUT_PATH = os.path.realpath(args.output)

    class Arguments(object): pass
    app_args = Arguments()
    app_args.config = os.path.realpath(args.config)
    app_args.input = os.path.realpath(args.input)
    app_args.output = os.path.join(OUTPUT_PATH, "base")
    app_args.debug = False

    with open(args.config) as fp:
        config_json = json.load(fp)

    Config._instance = None
    config = Config(config_json, app_args)
    importer.import_port_positions()

    if not (args.skip_cleanup or args.skip_convert):
        create_dir(OUTPUT_PATH, cleanup=True)
        logger.info("Cleaning up output folder")

    if not args.skip_convert:
        create_dir(config.dirs.output_dir, cleanup=True)
        create_dir(config.dirs.image_dir, cleanup=True)
        importer.process_gbrs_to_pngs()
    else:
        logger.info("Skipping image conversion")

    pair = config.diff_pairs[0]
    validate_diff_pair(pair)

    reference_layer = get_reference_layer(pair)
    im_ref = get_layer_image(reference_layer.file)
    hatch_configs = [
        # width (um), gap (um)
        (50, 50),
        (50, 150),
        (50, 250),
        (50, 350),
        (50, 450),
        (50, 550),
        (100, 100),
        (100, 200),
        (100, 300),
        (100, 400),
        (100, 500),
        (200, 100),
        (200, 200),
        (200, 300),
        (200, 400),
    ]
    get_variant_name = lambda hatch_config: "_".join(map(str, hatch_config))
    logger.info("Output variant parameters to csv file")
    with open(os.path.join(OUTPUT_PATH, "variants.csv"), "w+") as fp:
        fp.write("Name, Width (um), Gap (um)\n")
        for hatch_config in hatch_configs:
            fp.write(get_variant_name(hatch_config))
            fp.write(", ")
            fp.write(", ".join(map(str, hatch_config)))
            fp.write("\n")

    VARIANTS_DIR = os.path.join(OUTPUT_PATH, "variants")
    create_dir(VARIANTS_DIR, cleanup=not args.skip_cleanup)
    for hatch_config in hatch_configs:
        logger.info(f"Creating variant: {','.join(map(str, hatch_config))}")
        width_um, gap_um = hatch_config
        hatch_config_obj = HatchConfig(width_um, gap_um, COPLANAR_GAP_UM)
        im_hatch = create_hatched_plane(hatch_config_obj, pair, im_ref.size)
        im_ref_hatched = add_hatch_to_ref_plane(im_ref, im_hatch)
        # NOTE: flip to correct for flipping when loading it in
        im_ref_hatched = im_ref_hatched.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        # save to folder
        variant_name = get_variant_name(hatch_config)
        variant_path = os.path.join(VARIANTS_DIR, variant_name)
        if not os.path.exists(variant_path) or not args.skip_cleanup:
            try:
                shutil.rmtree(variant_path)
            except:
                pass
            shutil.copytree(config.dirs.output_dir, variant_path)
        else:
            logger.info(f"Skipping init of variant={variant_name}")
        variant_images_path = os.path.join(variant_path, "images")
        dst_path = os.path.join(variant_path, "images", f"{reference_layer.file}.png")
        im_ref_hatched.save(dst_path)

def create_dir(path, cleanup=False):
    directory_path = path
    if cleanup and os.path.exists(directory_path):
        shutil.rmtree(directory_path)
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)

def validate_diff_pair(pair):
    config = Config.get()
    port_indices = [pair.start_p, pair.stop_p, pair.start_n, pair.stop_n]
    ports = [config.ports[i] for i in port_indices]
    port = ports[0]
    signal_layer_index = port.layer
    reference_layer_index = port.plane
    port_width = port.width
    port_length = port.length
    is_same_signal = all((port.layer == signal_layer_index for port in ports))
    is_same_ref = all((port.plane == reference_layer_index for port in ports))
    is_same_width = all((port.width == port_width for port in ports))
    is_same_length = all((port.length == port_length for port in ports))
    assert(is_same_signal)
    assert(is_same_ref)
    assert(is_same_width)
    assert(is_same_length)

def get_reference_layer(pair):
    config = Config.get()
    ports = config.ports
    port = ports[pair.start_p]
    reference_layer_index = port.plane
    metal_layers = config.get_metals()
    reference_layer = metal_layers[reference_layer_index]
    assert(reference_layer.file != None)
    return reference_layer

def get_layer_image(name):
    config = Config.get()
    # NOTE: We flip the image so position lines up correctly
    #       Need to flip back any modified images when saving them
    filepath = os.path.join(config.dirs.image_dir, f"{name}.png")
    im = PIL.Image.open(filepath)
    im_flip = im.transpose(PIL.Image.FLIP_TOP_BOTTOM)
    im_gray = im_flip.convert("L")
    im_thresh = im_gray.point(lambda p: 255 if p < config.nanomesh.threshold else 0)
    return im_thresh

def create_hatched_plane(hatch_config: HatchConfig, pair, im_size):
    # hatch properties
    hatch_width_um = hatch_config.width_um
    hatch_gap_um = hatch_config.gap_um
    coplanar_spacing_um = hatch_config.coplanar_um
    hatch_size_um = hatch_width_um + hatch_gap_um

    pcb_width_px, pcb_height_px = im_size
    pcb_width_um, pcb_height_um = pcb_width_px*PIXEL_SIZE_MICRONS, pcb_height_px*PIXEL_SIZE_MICRONS

    config = Config.get()
    port_indices = [pair.start_p, pair.stop_p, pair.start_n, pair.stop_n]
    ports = [config.ports[i] for i in port_indices]

    # port properties
    width_um = ports[0].width
    height_um = ports[1].length
    x_pos_um = ports[0].position[0]
    x_neg_um = ports[2].position[0]
    x_pos_um, x_neg_um = min(x_pos_um, x_neg_um), max(x_pos_um, x_neg_um)
    x_midline_um = (x_pos_um + x_neg_um)/2
    y_start_um = ports[0].position[1]
    y_end_um = ports[1].position[1]
    y_start_um, y_end_um = min(y_start_um, y_end_um), max(y_start_um, y_end_um)
    y_start_um += height_um/2
    y_end_um -= height_um/2

    # create coplanar x axes
    x_coplanar_left_um = x_pos_um - width_um/2 - coplanar_spacing_um
    x_coplanar_right_um = x_neg_um + width_um/2 + coplanar_spacing_um
    x_coplanar_left_um = max(x_coplanar_left_um - hatch_width_um/2, hatch_width_um/2)
    x_coplanar_right_um = min(x_coplanar_right_um + hatch_width_um/2, pcb_width_um - hatch_width_um/2)

    # determine how many hatches we can fit
    y_spacing_um = hatch_size_um * (2**0.5)
    y_dist_um = y_end_um - y_start_um
    k = y_dist_um / y_spacing_um
    total_spans = math.floor(k)
    assert(total_spans >= 1)
    span_error = k - total_spans
    # print(f"k={k}, spans={total_spans}, error={span_error}, bridge={span_error/2}")

    # determine how we connect ports to hatch
    y_spans_um = total_spans*y_spacing_um
    y_remain_um = y_dist_um - y_spans_um
    y_bridge_um = y_remain_um/2
    is_inner = span_error > 0.25
    # print(f"is_inner={is_inner}")

    # create points for hatch midline and outer line
    y_midline_points_um = (np.arange(total_spans+1) * y_spacing_um) + y_bridge_um + y_start_um
    y_outer_points_um = (np.arange(total_spans) * y_spacing_um) + y_bridge_um + y_spacing_um/2 + y_start_um
    x_hatch_left_um = x_midline_um - y_spacing_um/2
    x_hatch_right_um = x_midline_um + y_spacing_um/2
    inner_hatch_indices = range(1, total_spans) if not is_inner else range(0, total_spans+1)
    inner_hatch_indices = list(inner_hatch_indices)

    # hatch consists of line segments and circular joins
    hatch_points = []
    hatch_lines = []

    # hatch connection points
    for i in inner_hatch_indices:
        hatch_points.append((x_midline_um, y_midline_points_um[i]))
    for y in y_outer_points_um:
        hatch_points.append((x_hatch_left_um, y))
        hatch_points.append((x_hatch_right_um, y))
    hatch_points.append((x_pos_um, y_start_um))
    hatch_points.append((x_neg_um, y_start_um))
    hatch_points.append((x_pos_um, y_end_um))
    hatch_points.append((x_neg_um, y_end_um))

    # create body of hatch
    for i in inner_hatch_indices:
        midpoint = (x_midline_um, y_midline_points_um[i])
        if (i-1) >= 0:
            hatch_lines.append((midpoint, (x_hatch_left_um, y_outer_points_um[i-1])))
            hatch_lines.append((midpoint, (x_hatch_right_um, y_outer_points_um[i-1])))
        if i < total_spans:
            hatch_lines.append((midpoint, (x_hatch_left_um, y_outer_points_um[i])))
            hatch_lines.append((midpoint, (x_hatch_right_um, y_outer_points_um[i])))
    # different ways of connecting ports to hatch
    if is_inner:
        # connect port to midline
        midpoint = (x_midline_um, y_midline_points_um[0])
        hatch_lines.append((midpoint, (x_pos_um, y_start_um)))
        hatch_lines.append((midpoint, (x_neg_um, y_start_um)))
        midpoint = (x_midline_um, y_midline_points_um[-1])
        hatch_lines.append((midpoint, (x_pos_um, y_end_um)))
        hatch_lines.append((midpoint, (x_neg_um, y_end_um)))
        # connector port to coplanar
        # hatch_lines.append(((x_coplanar_left_um, y_midline_points_um[0]), (x_pos_um, y_start_um)))
        # hatch_lines.append(((x_coplanar_right_um, y_midline_points_um[0]), (x_neg_um, y_start_um)))
        # hatch_lines.append(((x_coplanar_left_um, y_midline_points_um[-1]), (x_pos_um, y_end_um)))
        # hatch_lines.append(((x_coplanar_right_um, y_midline_points_um[-1]), (x_neg_um, y_end_um)))
        # hatch_points.append((x_coplanar_right_um, y_midline_points_um[0]))
        # hatch_points.append((x_coplanar_left_um, y_midline_points_um[-1]))
        # hatch_points.append((x_coplanar_left_um, y_midline_points_um[0]))
        # hatch_points.append((x_coplanar_right_um, y_midline_points_um[-1]))
    else:
        # connect port to outer hatch points
        hatch_lines.append(((x_pos_um, y_start_um), (x_hatch_left_um, y_outer_points_um[0])))
        hatch_lines.append(((x_neg_um, y_start_um), (x_hatch_right_um, y_outer_points_um[0])))
        hatch_lines.append(((x_pos_um, y_end_um), (x_hatch_left_um, y_outer_points_um[-1])))
        hatch_lines.append(((x_neg_um, y_end_um), (x_hatch_right_um, y_outer_points_um[-1])))

    # connect hatch to coplanar ground planes
    if (x_hatch_left_um-hatch_width_um/2) > x_coplanar_left_um:
        x_coplanar_hatch_gap_um = x_hatch_left_um - x_coplanar_left_um
        for y in y_outer_points_um:
            # connect diagonally
            hatch_lines.append(((x_coplanar_left_um, y-x_coplanar_hatch_gap_um), (x_hatch_left_um, y)))
            hatch_lines.append(((x_coplanar_left_um, y+x_coplanar_hatch_gap_um), (x_hatch_left_um, y)))
            hatch_lines.append(((x_coplanar_right_um, y-x_coplanar_hatch_gap_um), (x_hatch_right_um, y)))
            hatch_lines.append(((x_coplanar_right_um, y+x_coplanar_hatch_gap_um), (x_hatch_right_um, y)))
            # connect horizontally
            # hatch_lines.append(((x_coplanar_left_um, y), (x_hatch_left_um, y)))
            # hatch_lines.append(((x_coplanar_right_um, y), (x_hatch_right_um, y)))

    # blit to bitmap (255 means empty, 0 means copper)
    im_hatch = PIL.Image.new("L", im_size, 255)
    drawer = PIL.ImageDraw.Draw(im_hatch)
    as_coord = lambda p: tuple(map(int, p))
    to_px = lambda p: tuple((int(x/PIXEL_SIZE_MICRONS) for x in p))
    hatch_width_px = int(hatch_width_um/PIXEL_SIZE_MICRONS)
    colour = 0
    for hatch_line in hatch_lines:
        points = list(map(lambda p: as_coord(to_px(p)), hatch_line))
        drawer.line(points, width=hatch_width_px, fill=colour)
    for hatch_point in hatch_points:
        drawer.circle(hatch_point, radius=hatch_width_px/2, fill=colour)
    return im_hatch

def add_hatch_to_ref_plane(im_ref, im_hatch):
    im_ref_inv = PIL.ImageOps.invert(im_ref)
    im_hatch_inv = PIL.ImageOps.invert(im_hatch)
    im_inv = PIL.ImageChops.add(im_ref_inv, im_hatch_inv)
    # im = PIL.ImageOps.invert(im_inv)
    return im_inv

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
