"""
kicad_testpoints
Command line tool which exports the position of pads from a PCB to create a test point document
"""

import pandas
import numpy as np
import pcbnew
import logging


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


def get_pad_locations(points_df, board, use_drill_center=False):
    """
    Source format:
    + source ref des
    + pad number

    Output needs to be
    + x,y in mm
    + side
    + rotation
    + leave 'ref des' unallocated to allow the user to set the ref des for use with kicad-parts-placer
    """

    # bounding_box = board.GetBoardEdgesBoundingBox()

    points_df["pad number"] = np.array(points_df["pad number"], dtype=int)
    """
    cycle through parts
    get matching ref des
    find matching pad
    get center, apply class changes
    """
    # GetCenter GetName GetOrientation GetPosition GetSize HasHole GetNumber GetParentAsString
    points_df["pad"] = [None] * len(points_df)
    modules = []
    for ref_des in points_df["source ref des"]:
        module = board.FindFootprintByReference(ref_des)
        if module is None:
            raise UserWarning(f"Ref Des {ref_des} not found")
        modules.append(module)
    points_df["part value"] = [module.GetValue() for module in modules]
    points_df["side"] = [
        "TOP" if module.GetLayer() == 0 else "BOTTOM" for module in modules
    ]
    for i, row in points_df.iterrows():
        ref_des = row["source ref des"]
        module = board.FindFootprintByReference(ref_des)
        if not module:
            raise UserWarning("Ref Des %s not found", ref_des)

        found = False
        for pad in module.Pads():
            if str(pad.GetNumber()) == str(row["pad number"]):
                # (pad.GetName() == row["pad name"]) or
                points_df.loc[i, "pad"] = pad
                found = True
                break
        if found is False:
            nums = [str(pad.GetNumber()) for pad in module.Pads()]
            raise UserWarning(
                f"Pad {row['pad number']} not found in module {ref_des} ({nums})"
            )

    data = {}
    for f in ["x", "y", "rotation", "smt", "net"]:
        data[f] = []

    center = pcbnew.VECTOR2I_MM(0, 0)
    if use_drill_center:
        design_settings = board.GetDesignSettings()
        center = design_settings.GetAuxOrigin()

    log_ = logging.getLogger()
    log_.info("Center: %s", center)
    for _, row in points_df.iterrows():
        pad = row["pad"]
        if pad is None:
            raise UserWarning(f"Pad or part not found, {row}")
        x = pad.GetCenter()[0] - center.x
        y = pad.GetCenter()[1] - center.y
        data["x"].append(round(pcbnew.ToMM(x), 4))
        data["y"].append(round(pcbnew.ToMM(y), 4))
        data["rotation"].append(pad.GetOrientationDegrees())
        data["smt"].append(not pad.HasHole())
        data["net"].append(pad.GetShortNetname())

    points_df = points_df.drop(columns=["pad"])
    points_df = points_df.join(pandas.DataFrame(data))

    # distances = dict()
    # for name in points_df['test point ref des']:
    #    distances[name] = calc_probe_distance(name, points_df)

    # distances_df = pandas.DataFrame(distances)
    # print(distances_df)
    # distances_df['test point ref des'] = distances_df.index

    # points_df=points_df.merge(distances_df, on=['test point ref des'])
    return points_df
