'''
kicad_testpoints
Command line tool which exports the position of pads from a PCB to create a test point document
'''
import pcbnew
import pandas
import numpy as np


# the internal coorinate space of pcbnew is 1E-6 mm. (a millionth of a mm)
# the coordinate 121550000 corresponds to 121.550000
SCALE = 1/1e-6

def calc_probe_distance(name, probes_df):
    '''
    Calculate distance to all probes to this one. Return dict of distances.
    '''
    distances = dict();
    probe = probes_df[probes_df['test point ref des'] == name].iloc[0]
    for _, line in probes_df.iterrows():
        dist = [line['x'] - probe['x'], line['y'] - probe['y']]
        distances[line['test point ref des']] = (dist[0]**2 + dist[1]**2)**0.5
    return distances


def get_pad_locations(points_df, board):
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

    scale = SCALE
    bounding_box = board.GetBoardEdgesBoundingBox()

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
            if (pad.GetName() == row["pad name"]) or (str(pad.GetNumber()) == str(row["pad number"])):
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

    distances = dict()
    for name in points_df['test point ref des']:
        distances[name] = calc_probe_distance(name, points_df)

    distances_df = pandas.DataFrame(distances)
    print(distances_df)
    distances_df['test point ref des'] = distances_df.index

    points_df=points_df.merge(distances_df, on=['test point ref des'])
