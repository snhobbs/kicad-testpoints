"""Console script for kicad_testpoints."""

import logging

import click
import pandas as pd
import pcbnew
import sys
from pathlib import Path

from . import file_io
from . import kicad_testpoints

_log = logging.getLogger("kicad_testpoints")


@click.option("--debug", is_flag=True, help="")
@click.version_option()
@click.group()
def gr1(debug):
    _log.setLevel(logging.INFO)
    if debug:
        _log.setLevel(logging.DEBUG)
    return 0


@gr1.command(
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
def from_spreadsheet(pcb, points, out, drill_center, inplace):
    if inplace:
        out = points
    elif out is None:
        msg = "Either the inplace flag needs to be set or the --out option set"
        _log.error(msg)
        return sys.exit(1)

    board_path = Path(pcb).absolute()
    assert board_path.exists()
    print(board_path)
    board = pcbnew.LoadBoard(board_path.as_posix())
    points_df = file_io.read_file_to_df(points)
    pads = kicad_testpoints.get_pads(
        (
            (line["source ref des"], (line["source pad"]))
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
    return sys.exit(0)


@gr1.command(
    help="Pull out the position and net for all pads with a test point property set."
)
@click.option("--pcb", type=str, required=True, help="Source PCB file")
@click.option("--out", type=str, required=True, help="Output spreadsheet")
@click.option(
    "--drill-center", is_flag=True, help="Use drill/file center as reference coordinate"
)
def by_fab_setting(pcb, out, drill_center):
    board_path = Path(pcb).absolute()
    assert board_path.exists()
    print(board_path)
    board = pcbnew.LoadBoard(board_path.as_posix())
    pads = kicad_testpoints.get_pads_by_property(board)

    if len(pads) == 0:
        _log.warning("No pads with fabrication setting found")
        return sys.exit(1)

    assert len(pads) > 0
    settings = kicad_testpoints.Settings()
    settings.use_aux_origin = drill_center

    report = kicad_testpoints.build_test_point_report(board, settings, pads)
    report_df = pd.DataFrame(report)
    file_io.write(report_df, out)
    return sys.exit(0)


def main():
    return gr1()


if __name__ == "__main__":
    logging.basicConfig()
    _log.setLevel(logging.INFO)
    main()  # pragma: no cover
