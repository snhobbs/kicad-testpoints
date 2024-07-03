# kicad-testpoints

CLI to generate a [JigsApp](https://www.thejigspp.com) compatible test point report for generating bed-of-nails jigs. Specify any pad as a test pad.

## KiCAD Plugin
This is the command line tool based on reference designator and pad number.
For the action plugin see [snhobbs/kicad-testpoints-pcm](https://github.com/snhobbs/kicad-testpoints-pcm).

The plugin is generates the same report as the CLI except it can be used entirely within the KiCAD user interface (no terminals required) and uses the fabrication property of the pads instead of their pad number and ref des.

### Watch the plugin introduction
[![Watch the video](https://img.youtube.com/vi/Z7aEWe4d0jE/hqdefault.jpg)](https://www.youtube.com/embed/Z7aEWe4d0jE)

## Use
Any pad can be set as a test point.
Add the target pads to the spreadsheet input with the "source ref des" and the "pad number".

The CLI will pull out the related pad data and creates the report as a csv.

![Test Point Report CSV](test-point-report.png)

The generated report is consistent with the [kicad-parts-placer](https://github.com/snhobbs/kicad-parts-placer) CLI tool.

## Links
+ [Blog Post](https://www.thejigsapp.com/blog/2024/06/03/kicad-testpoints-plugin/)
+ [Video Introduction](https://www.youtube.com/watch?v=Z7aEWe4d0jE)
+ [TheJigsApp: Test Point Resports](https://www.thejigsapp.com/docs/test-point-report/).

## Test Points in other EDA Programs
+ [ Altium Designer ](https://www.altium.com/documentation/altium-designer/adding-testpoints-pcb)
+ [Cadence](https://resources.pcb.cadence.com/blog/2020-the-pcb-test-point-and-its-importance-to-circuit-board-manufacturing)
+ [PCB-Investigator](https://manual.pcb-investigator.com/pages/test_point_report)
+ [PADS](https://blogs.sw.siemens.com/electronic-systems-design/2020/04/21/test-point-placement-enhancement-in-pads-professional-vx-2-7/)

For more on generating test point reports see [this post](https://www.thejigsapp.com/docs/test-point-report/).
