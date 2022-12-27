# kicad-testpoints

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

