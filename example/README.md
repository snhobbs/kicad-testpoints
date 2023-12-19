# Example Test Pad Extraction

The example design here is pulled from kicad. I chose a random project to avoid any bias.
The board is done in discrete shapes instead of as a footprint and therefore has no defined center.
The board appears to have been placed randomly so will need centering. The designer will need to choose
a reference point. Here I have measured the x,y center and am using that as the center point.

The board size is 35x55mm and centered at [112.43016, 133.46636].

```sh
kicad_testpoints --pcb pocketbone-kicad/pocketbone-kicad.kicad_pcb --points points.xlsx --out points_out.xlsx -x 112.43016 -y 133.46636
```

The output positions and net type is used as an input to [TheJigsApp](thejigsapp.com) to generate test systems.
