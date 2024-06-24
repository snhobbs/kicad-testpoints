"""Console script for kicad_testpoints."""

import logging

import click
import pandas as pd
import pcbnew

from . import file_io
from . import kicad_testpoints

_log = None


@click.command(
    help="Takes a PCB & configuration data in mm, sets rotation and location on a new pcb"
)
@click.option("--pcb", type=str, required=True, help="Source PCB file")
@click.option(
    "--points", type=str, required=True, help="Spreadsheet configuration file"
)
@click.option("--out", type=str, required=False, help="Output spreadsheet")
@click.option(
    "--drill-center", is_flag=True, help="Use drill/file center as reference coordinate"
)
@click.option("--inplace", is_flag=True, help="Edit probe spreadsheet inplace")
@click.option("--debug", is_flag=True, help="")
def main(pcb, points, out, drill_center, inplace, debug):
    global _log
    _log = logging.getLogger()
    _log.setLevel(logging.WARNING)
    if debug:
        _log.setLevel(logging.DEBUG)

    if inplace:
        out = points
    elif out is None:
        msg = "Either the inplace flag needs to be set or the --out option set"
        raise ValueError(msg)

    board = pcbnew.LoadBoard(pcb)
    points_df = file_io.read_file_to_df(points)
    pads = kicad_testpoints.get_pads(
        (
            (line["source ref des"], int(line["source pad"]))
            for _, line in points_df.iterrows()
        ),
        board,
    )

    settings = kicad_testpoints.Settings()
    settings.use_aux_origin = drill_center

    report = kicad_testpoints.build_test_point_report(board, settings, pads)
    report_df = pd.DataFrame(report)
    # kicad_testpoints.write_csv(report, Path(out))
    file_io.write(report_df, out)


if __name__ == "__main__":
    logging.basicConfig()
    main()  # pragma: no cover
