"""
coverage.py
Tools to read a netlist, a testpoint report, and generate a coverage report.
"""

import csv
from pathlib import Path

_log = logging.getLogger("kicad_testpoints")

# Table of fields and how to get them
_fields = {
    "source ref des": (
        lambda p, **kwargs: p.GetParentFootprint().GetReferenceAsString()
    ),
    "source pad": (lambda p, **kwargs: p.GetNumber()),
    "net": get_net_name,
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
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        if fieldnames is not None:
            writer.writeheader()
        writer.writerows(data)


def build_test_point_report(
    board: pcbnew.BOARD, settings: Settings, pads: tuple[pcbnew.PAD]
) -> list[dict]:
    if settings.use_aux_origin:
        ds = board.GetDesignSettings()
        aux_origin = ds.GetAuxOrigin()
        if aux_origin is None:
            # Keep origin as 0,0
            _log.info("No aux origin returned. Using 0,0 as origin")
            settings.use_aux_origin = False

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


def get_pads_by_property(board: pcbnew.BOARD) -> tuple[pcbnew.PAD]:
    """
    Get list of matching pads from a list of (ref_des, pad_num)
    """
    test_point_property = 4
    pads = []
    for p in board.GetPads():
        if p.GetProperty() != test_point_property:
            continue
        pads.append(p)
    return pads
