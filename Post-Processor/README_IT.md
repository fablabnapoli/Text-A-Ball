#Text2GCode 

## Usage
python text2Gcode.py -X5 -Y30 -x10 -y10 -S1.2 -s1.2 -0"#MFR16" -1"Hello World" -2"@FabLabNapoli" > gcodeOut.gcode

* -X5: 							start position x for the first line
* -Y30:							start position y for the first line
* -x10:							line indentation
* -y10:							line height
* -S1.2:						Scale X
* -s1.2:							Scale Y
* -0"#MFR16":				First line
* -1"Hello World": 		Second line
* -2"@FabLabNapoli": 	Third line
* gcodeOut.gcode		Output file containing the tool path

The output:

![Example output](.\images\goodGcode.jpg)

## To Do List

- [x] Manage X offset between lines (-x option)
- [x] Manage Y offset between lines (-y options)
- [x] Manage start X,Y value (-X, -Y options)
- [ ] Auto center horizontally
- [ ] Auto center vertically
- [ ] Clean up the code 
- [ ] Move font-scale functionality in font-dictionary creation function (t2gLib.parse) **[optimization]**
- [ ] Do not rebuild the font-dictionary for each line to plot **[optimization]**