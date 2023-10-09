'''
kicad_testpoints
Command line tool which exports the position of pads from a PCB to create a test point document
'''


import logging
import pcbnew
import pandas
import click
import spreadsheet_wrangler
import numpy as np


# the internal coorinate space of pcbnew is 1E-6 mm. (a millionth of a mm)
# the coordinate 121550000 corresponds to 121.550000
SCALE = 1/1e-6


'''
Source format:
    + source ref des
    + pad number
    + pad name

Output needs to be
    + x,y in mm
    + side
    + rotation
    + leave 'ref des' unallocated to allow the user to set the ref des for use with kicad-parts-placer
'''


@click.command(help="Takes a PCB & configuration data in mm, sets rotation and location on a new pcb")
@click.option("--pcb", type=str, required=True, help="Source PCB file")
@click.option("--points", type=str, required=True, help="Spreadsheet configuration file")
@click.option("--out", type=str, required=False, help="Output spreadsheet")
@click.option("--center-x", "-x", type=float, default=0, help="")
@click.option("--center-y", "-y", type=float, default=0, help="")
#@click.option("--center-on-board", is_flag=True, help="Center group on board bounding box")
@click.option("--mirror", is_flag=True, help="Mirror parts, required for matching up the front and back of two boards")
@click.option("--inplace", is_flag=True, help="Edit probe spreadsheet inplace")
@click.option("--debug", is_flag=True, help="")
def main(pcb, points, out, center_x, center_y, mirror, inplace, debug):
    scale = SCALE
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
    bounding_box = board.GetBoardEdgesBoundingBox()

    points_df = spreadsheet_wrangler.read_file_to_df(points)
    points_df["pad number"] = np.array(points_df["pad number"], dtype=int)
    print(points_df)
    '''
    cycle through parts
    get matching ref des
    find matching pad
    get center, apply class changes
    '''
    #GetCenter GetName GetOrientation GetPosition GetSize HasHole GetNumber GetParentAsString
    points_df["pad"] = [None]*len(points_df)
    for i, row in points_df.iterrows():
        ref_des = row["source ref des"]
        module = board.FindFootprintByReference(ref_des)
        if not module:
            raise UserWarning("Ref Des %s not found", ref_des)
        for pad in module.Pads():
            if (pad.GetName() == row["pad name"]) or (int(pad.GetNumber()) == row["pad number"]):
                points_df.loc[i, "pad"] = pad
                break

    data = dict()
    for f in ['x', 'y', 'rotation','smt', 'side','net']:
        data[f] = []

    x_mult = -1 if mirror else 1

    for _, row in points_df.iterrows():
        pad = row['pad']
        x = (pad.GetCenter()[0]/SCALE - center_x)*x_mult
        y = pad.GetCenter()[1]/SCALE - center_y
        data['x'].append(round(x,4))
        data['y'].append(round(y,4))
        data['rotation'].append(pad.GetOrientationDegrees())
        data['smt'].append(not pad.HasHole())
        data['side'].append("TOP" if pad.GetLayer() == 0 else "BOTTOM")
        data['net'].append(pad.GetShortNetname())

    points_df=points_df.drop(columns=["pad"])

    points_df = points_df.join(pandas.DataFrame(data))
    points_df.to_excel(out)



if __name__ == "__main__":
    main()
