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
COPLANAR_WIDTH_UM = 200

class TaperConfig:
    def __init__(self, width, length, overlap, coplanar_gap, coplanar_width):
        self.width_um = width
        self.length_um = length
        self.overlap_um = overlap
        self.coplanar_gap_um = coplanar_gap
        self.coplanar_width_um = coplanar_width

def create_arg_parser():
    parser = argparse.ArgumentParser(
        prog="generate_tapers",
        description="Generate modified simulation files with varying taper configurations",
    )
    parser.add_argument("--config", dest="config", type=str, default="./simulation.json")
    parser.add_argument("-i", "--input", dest="input", type=str, default="./fab")
    parser.add_argument("-o", "--output", dest="output", type=str, default="./variants_simulation")
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

    signal_layer, ref_0_layer, ref_1_layer = get_port_layers(pair)
    im_ref_0 = get_layer_image(ref_0_layer.file)
    im_ref_1 = get_layer_image(ref_1_layer.file)
    im_signal = get_layer_image(signal_layer.file)

    taper_configs = [
        # width (um), length (um), overlap (um)
    ]
    for width in (150, 200, 250):
        for length in (100, 250, 500, 1000, 1500, 2000):
            for delta in (0.5, 0.75, 1.0, 1.25, 1.5):
                overlap = int(delta*length)
                taper_configs.append((width, length, overlap))

    get_variant_name = lambda taper_config: "_".join(map(str, taper_config))
    logger.info("Output variant parameters to csv file")
    with open(os.path.join(OUTPUT_PATH, "variants.csv"), "w+") as fp:
        fp.write("Name, Width (um), Length (um), Overlap (um)\n")
        for taper_config in taper_configs:
            fp.write(get_variant_name(taper_config))
            fp.write(", ")
            fp.write(", ".join(map(str, taper_config)))
            fp.write("\n")

    VARIANTS_DIR = os.path.join(OUTPUT_PATH, "variants")
    create_dir(VARIANTS_DIR, cleanup=not args.skip_cleanup)
    for taper_config in taper_configs:
        logger.info(f"Creating variant: {','.join(map(str, taper_config))}")
        width_um, length_um, overlap_um = taper_config
        taper_config_obj = TaperConfig(width_um, length_um, overlap_um, COPLANAR_GAP_UM, COPLANAR_WIDTH_UM)
        im_taper_0, im_taper_1 = create_taper(taper_config_obj, pair, im_signal.size)
        im_ref_0_taper = add_taper_to_ref_plane(im_taper_0, im_ref_0)
        im_ref_1_taper = add_taper_to_ref_plane(im_taper_1, im_ref_1)
        im_debug = create_debug_image(im_signal, im_ref_0, im_ref_1, im_taper_0, im_taper_1)
        # NOTE: flip to correct for flipping when loading it in
        im_ref_0_taper = im_ref_0_taper.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        im_ref_1_taper = im_ref_1_taper.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        im_debug = im_debug.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        # save to folder
        variant_name = get_variant_name(taper_config)
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
        im_ref_0_taper.save(os.path.join(variant_images_path, f"{ref_0_layer.file}.png"))
        im_ref_1_taper.save(os.path.join(variant_images_path, f"{ref_1_layer.file}.png"))
        im_debug.save(os.path.join(variant_images_path, f"{ref_0_layer.file}_{ref_1_layer.file}_taper_debug.png"))

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
    port_width = port.width
    port_length = port.length
    is_same_signal = all((port.layer == signal_layer_index for port in ports))
    is_same_width = all((port.width == port_width for port in ports))
    is_same_length = all((port.length == port_length for port in ports))
    assert(is_same_signal)
    assert(is_same_width)
    assert(is_same_length)
    assert(ports[0].plane == ports[2].plane)
    assert(ports[1].plane == ports[3].plane)

def get_port_layers(pair):
    config = Config.get()
    ports = config.ports
    port_0 = ports[pair.start_p]
    port_1 = ports[pair.stop_p]
    ref_0_layer_index = port_0.plane
    ref_1_layer_index = port_1.plane
    signal_layer_index = port_0.layer
    metal_layers = config.get_metals()
    ref_0_layer = metal_layers[ref_0_layer_index]
    ref_1_layer = metal_layers[ref_1_layer_index]
    signal_layer = metal_layers[signal_layer_index]
    assert(ref_0_layer.file != None)
    assert(ref_1_layer.file != None)
    assert(signal_layer.file != None)
    return (signal_layer, ref_0_layer, ref_1_layer)

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

def create_taper(taper_config: TaperConfig, pair, im_size):
    # taper properties
    taper_overlap_um = taper_config.overlap_um
    taper_width_um = taper_config.width_um
    taper_length_um = taper_config.length_um
    coplanar_gap_um = taper_config.coplanar_gap_um
    coplanar_width_um = taper_config.coplanar_width_um

    # port properties
    config = Config.get()
    port_indices = [pair.start_p, pair.stop_p, pair.start_n, pair.stop_n]
    ports = [config.ports[i] for i in port_indices]
    width_um = ports[0].width
    height_um = ports[1].length

    # common axes
    x_pos_um = ports[0].position[0]
    x_neg_um = ports[2].position[0]
    x_pos_um, x_neg_um = min(x_pos_um, x_neg_um), max(x_pos_um, x_neg_um)
    y_start_um = ports[0].position[1]
    y_end_um = ports[1].position[1]
    y_start_um, y_end_um = min(y_start_um, y_end_um), max(y_start_um, y_end_um)
    y_midline_um = int((y_start_um + y_end_um)/2)
    x_left_um = int(x_pos_um - width_um/2 - coplanar_gap_um - coplanar_width_um)
    x_right_um = int(x_neg_um + width_um/2 + coplanar_gap_um + coplanar_width_um)

    y_taper_top_um = y_midline_um - int(taper_overlap_um/2)
    y_taper_bottom_um = y_midline_um + int(taper_overlap_um/2)

    # blit to bitmap (255 means empty, 0 means copper)
    im_taper_0 = PIL.Image.new("L", im_size, 255)
    im_taper_1 = PIL.Image.new("L", im_size, 255)
    drawer_0 = PIL.ImageDraw.Draw(im_taper_0)
    drawer_1 = PIL.ImageDraw.Draw(im_taper_1)

    as_coord = lambda p: tuple(map(int, p))
    to_px = lambda p: tuple((int(x/PIXEL_SIZE_MICRONS) for x in p))

    def draw_triangle(drawer, start, width, height):
        p0 = (start[0]-width/2, start[1])
        p1 = (start[0]+width/2, start[1])
        p2 = (start[0], start[1]+height)
        points = (p0, p1,p2)
        points = [to_px(point) for point in points]
        drawer.polygon(points, fill=0)

    drawer_0.rectangle(tuple(map(to_px, ((x_left_um, y_start_um), (x_right_um, y_taper_top_um)))), fill=0)
    draw_triangle(drawer_0, (x_pos_um, y_taper_top_um), taper_width_um, taper_length_um)
    draw_triangle(drawer_0, (x_neg_um, y_taper_top_um), taper_width_um, taper_length_um)
    # draw_triangle(drawer_0, (x_left_um+coplanar_width_um/2, y_taper_top_um), coplanar_width_um, taper_length_um)
    # draw_triangle(drawer_0, (x_right_um-coplanar_width_um/2, y_taper_top_um), coplanar_width_um, taper_length_um)

    fill = (0,128,128,128)
    drawer_1.rectangle(tuple(map(to_px, ((x_left_um, y_taper_bottom_um), (x_right_um, y_end_um)))), fill=0)
    draw_triangle(drawer_1, (x_pos_um, y_taper_bottom_um), taper_width_um, -taper_length_um)
    draw_triangle(drawer_1, (x_neg_um, y_taper_bottom_um), taper_width_um, -taper_length_um)
    # draw_triangle(drawer_1, (x_left_um+coplanar_width_um/2, y_taper_bottom_um), coplanar_width_um, -taper_length_um)
    # draw_triangle(drawer_1, (x_right_um-coplanar_width_um/2, y_taper_bottom_um), coplanar_width_um, -taper_length_um)

    if ports[0].position[1] < ports[1].position[1]:
        return (im_taper_0, im_taper_1)
    else:
        return (im_taper_1, im_taper_0)

def add_taper_to_ref_plane(im_ref, im_taper):
    im_ref_inv = PIL.ImageOps.invert(im_ref)
    im_taper_inv = PIL.ImageOps.invert(im_taper)
    im_inv = PIL.ImageChops.add(im_ref_inv, im_taper_inv)
    # im = PIL.ImageOps.invert(im_inv)
    return im_inv

def create_debug_image(im_signal, im_ref_0, im_ref_1, im_taper_0, im_taper_1):
    def convert_to_alpha(im, colour):
        im_mask = 255 - np.array(im, dtype=np.uint16)
        im_mask = im_mask.reshape(im_mask.shape + (1,))
        total_channels = 4
        shape = im_mask.shape[:2] + (total_channels,)
        im_fill = np.full(shape, colour, dtype=np.uint16)
        im_out = im_fill*im_mask
        im_out = np.clip(im_out, a_min=0, a_max=255)
        opacity = colour[3]
        im_out[:,:,3:4] = np.clip(im_mask, a_min=0, a_max=1)*opacity
        im_out = im_out.astype(np.uint8)
        im_out = PIL.Image.fromarray(im_out, mode="RGBA")
        return im_out

    im_ref_0 = convert_to_alpha(im_ref_0, (0,255,0,64))
    im_ref_1 = convert_to_alpha(im_ref_1, (0,0,255,64))
    im_signal = convert_to_alpha(im_signal, (255,0,0,80))
    im_taper_0 = convert_to_alpha(im_taper_0, (128,128,0,100))
    im_taper_1 = convert_to_alpha(im_taper_1, (0,128,128,100))

    im_out = PIL.Image.new("RGBA", im_signal.size, (255,255,255,255))
    im_out = PIL.Image.alpha_composite(im_out, im_ref_0)
    im_out = PIL.Image.alpha_composite(im_out, im_ref_1)
    im_out = PIL.Image.alpha_composite(im_out, im_signal)
    im_out = PIL.Image.alpha_composite(im_out, im_taper_0)
    im_out = PIL.Image.alpha_composite(im_out, im_taper_1)
    return im_out

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
