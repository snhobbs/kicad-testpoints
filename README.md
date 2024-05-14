# kicad-testpoints

## Project Scope
+ Simplify the process of building a test & programming jig for a KiCAD design.
+ Export centroid like data for individual pads

## Basic Goals
+ Call out a list of pads and vias for use as test points
+ Output in a format that is consistant with [kicad-parts-placer](https://github.com/snhobbs/kicad-parts-placer).

## Related Projects
+ [ Altium Designer ](https://www.altium.com/documentation/altium-designer/adding-testpoints-pcb)



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
+ Vias need to be a seperate flow
    + net
    + class
    + x, y roughly (auto chooses the closest point)
