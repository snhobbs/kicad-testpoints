"""
kicad_testpoints
Command line tool which exports the position of pads from a PCB to create a test point document
"""

import csv
import logging
from pathlib import Path

import pcbnew

_log = logging.getLogger("kicad_testpoints")


def calc_probe_distance(name, probes_df):
    """
    Calculate distance to all probes to this one. Return dict of distances.
    """
    distances = {}
    probe = probes_df[probes_df["test point ref des"] == name].iloc[0]
    for _, line in probes_df.iterrows():
        dist = [line["x"] - probe["x"], line["y"] - probe["y"]]
        distances[line["test point ref des"]] = (dist[0] ** 2 + dist[1] ** 2) ** 0.5
    return distances


class Settings:
    """
    All the options that can be passed
    """

    def __init__(self):
        self.use_aux_origin: bool = False


def get_pad_side(p: pcbnew.PAD, **kwargs):
    """
    As footprints can be on the top or bottom and the pad position is relative
    to the footprint we need to use both the footprint and the pad position to get
    the correct side. As the top layer/side is 0 then we can do the following.
    """
    fp: pcbnew.FOOTPRINT = p.GetParentFootprint()
    return "BOTTOM" if (fp.GetSide() - p.GetLayer()) else "TOP"


def calc_pad_position(center: tuple[float, float], origin: tuple[float, float]):
    """
    Calculate pad position as relative to the origin and in cartesian coordinates.
    The origin and center should be in native kicad pixel coordinates.
    """
    return (center[0] - origin[0]), -1 * (center[1] - origin[1])


def get_pad_position(p: pcbnew.PAD, settings: Settings) -> tuple[float, float]:
    """
    Get the center of the pad, the origin setting, and the quadrant setting,
    calculate the transformed position.

    The position internal to kicad never changes. The position is always the distance from
    the top left with x increasing to the right and y increasing down.

    Take the origin location and calculate the distance. Then multiple the axis so it is
    increasing in the desired direction. To match the gerbers this should be increasing right and up.
    """
    board = p.GetBoard()
    ds = board.GetDesignSettings()
    origin = (0, 0)
    if settings.use_aux_origin:
        origin = pcbnew.ToMM(ds.GetAuxOrigin())
    center = [round(pt, 4) for pt in pcbnew.ToMM(p.GetCenter())]
    position = calc_pad_position(origin=origin, center=center)
    return [round(pt, 4) for pt in position]


# Table of fields and how to get them
_fields = {
    "source ref des": (
        lambda p, **kwargs: p.GetParentFootprint().GetReferenceAsString()
    ),
    "source pad": (lambda p, **kwargs: p.GetNumber()),
    "net": (lambda p, **kwargs: p.GetShortNetname()),
    "net class": (lambda p, **kwargs: p.GetNetClassName()),
    "side": get_pad_side,
    "x": (lambda p, **kwargs: get_pad_position(p, **kwargs)[0]),
    "y": (lambda p, **kwargs: get_pad_position(p, **kwargs)[1]),
    "pad type": (lambda p, **kwargs: "THRU" if p.HasHole() else "SMT"),
    "footprint side": (
        lambda p, **kwargs: "BOTTOM" if p.GetParentFootprint().GetSide() else "TOP"
    ),
}


def write_csv(data: list[dict], filename: Path):
    fieldnames = data[0].keys()
    with filename.open("w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if fieldnames is not None:
            writer.writeheader()
        writer.writerows(data)


def build_test_point_report(
    board: pcbnew.BOARD, settings: Settings, pads: tuple[pcbnew.PAD]
) -> list[dict]:
    if pads:
        assert isinstance(pads[0], pcbnew.PAD)
    return [
        {key: value(p, settings=settings) for key, value in _fields.items()}
        for p in pads
    ]


def get_pads(
    pad_pair: tuple[tuple[str, int]], board: pcbnew.BOARD
) -> tuple[pcbnew.PAD]:
    """
    Get list of matching pads from a list of (ref_des, pad_num)
    """
    pads = []
    for ref_des, pad_number in pad_pair:
        module = board.FindFootprintByReference(ref_des)
        if not module:
            msg = "Ref Des %s not found"
            raise UserWarning(msg, ref_des)

        found = False
        for pad in module.Pads():
            if str(pad.GetNumber()) == str(pad_number):
                pads.append(pad)
                found = True
                break
        if found is False:
            nums = [str(pad.GetNumber()) for pad in module.Pads()]
            msg = f"Pad {pad_number} not found in module {ref_des} ({nums})"
            raise UserWarning(msg)

    return pads
