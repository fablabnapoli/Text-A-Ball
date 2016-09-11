"""
Engrave-line derivated Lib


Copyright (C) <2008>  <Lawrence Glaister> <ve7it at shaw dot ca>
based on work by John Thornton  -- GUI framwork from arcbuddy.py
Ben Lipkowitz  (fenn)-- cxf2cnc.py v0.5 font parsing code
"""

import re

#====================================================================
class Character:
    def __init__(self, key):
        self.key = key
        self.stroke_list = []

    def __repr__(self):
        return "%s" % (self.stroke_list)

    def get_xmax(self):
        try: return max([s.xmax for s in self.stroke_list[:]])
        except ValueError: return 0

    def get_ymax(self):
        try: return max([s.ymax for s in self.stroke_list[:]])
        except ValueError: return 0

#====================================================================
class Line:

    def __init__(self, coords):
        self.xstart, self.ystart, self.xend, self.yend = coords
        self.xmax = max(self.xstart, self.xend)
        self.ymax = max(self.ystart, self.yend)

    def __repr__(self):
        return "Line([%s, %s, %s, %s])" % (self.xstart, self.ystart, self.xend, self.yend)


#=====================================================================
# This routine parses the .cxf font file and builds a font dictionary of
# line segment strokes required to cut each character.
# Arcs (only used in some fonts) are converted to a number of line
# segemnts based on the angular length of the arc. Since the idea of
# this font description is to make it support independant x and y scaling,
# we can not use native arcs in the gcode.
#=====================================================================
def parse(file):
    font = {}
    key = None
    num_cmds = 0
    line_num = 0
    for text in file:
        #format for a typical letter (lowercase r):
        ##comment, with a blank line after it
        #
        #[r] 3
        #L 0,0,0,6
        #L 0,6,2,6
        #A 2,5,1,0,90
        #
        line_num += 1
        end_char = re.match('^$', text) #blank line
        if end_char and key: #save the character to our dictionary
            font[key] = Character(key)
            font[key].stroke_list = stroke_list
            font[key].xmax = xmax
            if (num_cmds != cmds_read):
                print "(warning: discrepancy in number of commands %s, line %s, %s != %s )" % (fontfile, line_num, num_cmds, cmds_read)

        new_cmd = re.match('^\[(.*)\]\s(\d+)', text)
        if new_cmd: #new character
            key = new_cmd.group(1)
            num_cmds = int(new_cmd.group(2)) #for debug
            cmds_read = 0
            stroke_list = []
            xmax, ymax = 0, 0

        line_cmd = re.match('^L (.*)', text)
        if line_cmd:
            cmds_read += 1
            coords = line_cmd.group(1)
            coords = [float(n) for n in coords.split(',')]
            stroke_list += [Line(coords)]
            xmax = max(xmax, coords[0], coords[2])

        arc_cmd = re.match('^A (.*)', text)
        if arc_cmd:
            cmds_read += 1
            coords = arc_cmd.group(1)
            coords = [float(n) for n in coords.split(',')]
            xcenter, ycenter, radius, start_angle, end_angle = coords
            # since font defn has 