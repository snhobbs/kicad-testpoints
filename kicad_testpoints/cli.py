"""Console script for kicad_testpoints."""
import sys
import os
import click
import jinja2
import pandas
import logging
import spreadsheet_wrangler
import pcbnew
from . import kicad_testpoints


template = jinja2.Template('''function get_design_probes(ground_height = -1, signal_height_dz = -0.5, power_height_dz = -1) = [
    {% for line in lines -%}
    [{{line.x}}, {{line.y}}, ground_height + power_height_dz],  //  {{line["net"]}} {{line["ref des"]}}
    {% endfor -%}
];
''')


@click.command(help="Takes a PCB & configuration data in mm, sets rotation and location on a new pcb")
@click.option("--points", type=str, required=True, help="Spreadsheet configuration file")
@click.option("--out", type=str, required=False, help="Output openscad file name")
@click.option("--debug", is_flag=True, help="")
def data_frame_to_openscad(points, out, debug):
    '''
    Generate pin and probe list from a configuration
    '''
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)

    if not out:
        out = points.splitext[0]) + ".scad"
    points_df = pandas.read_excel(points)
    lines = [line for _, line in points_df.iterrows()]
    string = template.render(lines=lines)

    with open(out, 'w') as f:
        f.write(string)


@click.command(help="Takes a PCB & configuration data in mm, sets rotation and location on a new pcb")
@click.option("--pcb", type=str, required=True, help="Source PCB file")
@click.option("--points", type=str, required=True, help="Spreadsheet configuration file")
@click.option("--out", type=str, required=False, help="Output spreadsheet")
@click.option("--center-x", "-x", type=float, default=0, help="")
@click.option("--center-y", "-y", type=float, default=0, help="")
#  @click.option("--center-on-board", is_flag=True, help="Center group on board bounding box")
@click.option("--mirror", is_flag=True, help="Mirror parts, required for matching up the front and back of two boards")
@click.option("--inplace", is_flag=True, help="Edit probe spreadsheet inplace")
@click.option("--debug", is_flag=True, help="")
def main(pcb, points, out, center_x, center_y, mirror, inplace, debug):

    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)

    if inplace:
        out = points
    else:
        if out is None:
            raise ValueError("Either the inplace flag needs to be set or the --out option set")

    board = pcbnew.LoadBoard(pcb)
    points_df = spreadsheet_wrangler.read_file_to_df(points)
    df_filled = kicad_testpoints.get_pad_locations(points_df, board)
    df_filled.to_excel(out)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
