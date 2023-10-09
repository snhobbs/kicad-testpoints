'''
Generate pin and probe list from a configuration
'''

import jinja2
import pandas
import click
import logging

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
def main(points, out, debug):
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)

    if not out:
        out = ".".join(points.split('.')[:-1])+".scad"
    points_df = pandas.read_excel(points)
    lines = [line for _, line in points_df.iterrows()]
    string = template.render(lines=lines)

    with open(out, 'w') as f:
        f.write(string)

if __name__ == "__main__":
    main()
