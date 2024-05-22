# kicad-testpoints

## Project Scope
+ Simplify the process of building a test & programming jig for a KiCAD design.
+ Export centroid like data for individual pads

## Basic Goals
+ Call out a list of pads and vias for use as test points
+ Output in a format that is consistent with [kicad-parts-placer](https://github.com/snhobbs/kicad-parts-placer).


+ Describe the via or pad to add a test point to
+ Offsets can be added to put the pin off center of the pad
+ Format:
    + ref des
    + pad
    + class
    + net
    + net class (signal, ground, power, ...)
    + ... additional data for other tools
+ Config script
    + Defines the classes of contacts.
    + Probe type
    + Offset
    + Vertical position relative to ground pins
+ Vias need to be a separate flow
    + net
    + class
    + x, y roughly (auto chooses the closest point)


## Test Points in other EDA Programs
+ [ Altium Designer ](https://www.altium.com/documentation/altium-designer/adding-testpoints-pcb)
+ [Cadence](https://resources.pcb.cadence.com/blog/2020-the-pcb-test-point-and-its-importance-to-circuit-board-manufacturing)
+ [PCB-Investigator](https://manual.pcb-investigator.com/pages/test_point_report)
+ [PADS](https://blogs.sw.siemens.com/electronic-systems-design/2020/04/21/test-point-placement-enhancement-in-pads-professional-vx-2-7/)

For more on generating test point reports see [this post](https://www.thejigsapp.com/docs/test-point-report/).
