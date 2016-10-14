import sys
import re

from math import *

class Character: #engrave-lines
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

class Line: #engrave-lines

    def __init__(self, coords):
        self.xstart, self.ystart, self.xend, self.yend = coords
        self.xmax = max(self.xstart, self.xend)
        self.ymax = max(self.ystart, self.yend)

    def __repr__(self):
        return "Line([%s, %s, %s, %s])" % (self.xstart, self.ystart, self.xend, self.yend)

def sanitize(string): #engrave-lines
    retval = ''
    good=' ~!@#$%^&*_+=-{}[]|\:;"<>,./?'
    for char in string:
        if char.isalnum() or good.find(char) != -1:
            retval += char
        else: retval += ( ' 0x%02X ' %ord(char))
    return retval

#================= risePen ======================
def risePen(gcode):
   """
   La funzione genera le istruzioni G-Code per sollevare il cursore 
   dalla superficie di stampa.

   Keyword arguments:
   gcode -- array/stringa a cui accodare i comandi G-Code
   """
   gcode.append("M300 S46")
   #gcode.append("G0 Z0.1000")

#================= lowerPen =====================
def lowerPen(gcode):
   """
   La funzione genera le istruzioni G-Code per abbassare il cursore 
   a contatto con la superficie di stampa.

   Keyword arguments:
   gcode -- array/stringa a cui accodare i comandi G-Code
   """
   gcode.append("M300 S43")
   #gcode.append("G0 Z0")

#================= travel =======================
def travel(gcode, x, y):
    """
    Con travel si intende lo spostamento del cursore senza tracciare linee
    L'operazione di "travel" è l'opposto dell'operzione plot (spostamento con 
    tracciatura).
    La funzione genera le istruzioni G-Code per spostare la penna dalla 
    posizione attuale alla posizione x,y senza tracciare linee.
    Il G-code generato solleva il cursore, lo sposta ed lo abbassa 
    nuovamente.
    
    Keyword arguments:
    gcode -- array/stringa a cui accodare i comandi G-Code
    x -- Coordinata x a cui spostare il cursore
    y -- Coordinata y a cui spostare il cursore
    """
    gcode.append(' ')
    gcode.append('; <Start travelling> ')
    risePen(gcode)
    gcode.append('G0 X%.4f Y%.4f' %(x,y))
    lowerPen(gcode)
    gcode.append('; <End travelling> ')
    gcode.append(' ')


#================= postamble ====================
def postamble(gcode, postamble):
    """
    La funzione genera le istruzioni di chiusura del G-Code. (es sollevamento
    finale cursore, spegnimento macchina ecc).
    Vine richiamata la funzione risePen e successivamente accodate le 
    istruzioni indicate nella variabile Postamble.
    
    Keyword arguments:
    gcode -- array/stringa a cui accodare i comandi G-Code
    """
    gcode.append('; <Start Postable> ')
    risePen(gcode)
    gcode+=postamble
    gcode.append('; <End Postable> ')

#================= preamble =====================
def preamble(gcode, preamble):
    """
    La funzione genera le istruzioni di apertura del G-Code. (es sollevamento
    cursore, impostazione sistema metrico,  ecc).
    Vine richiamata la funzione risePen e successivamente accodate le 
    istruzioni indicate nella variabile Postamble.
    
    Keyword arguments:
    gcode -- array/stringa a cui accodare i comandi G-Code
    """
    gcode.append('; <Start Preamble> ')
    gcode+=preamble
    risePen(gcode)
    gcode.append('; <End Preamble> ')
    gcode.append(' ')

#================= transform =====================
def transform(x, y, Xscale, Yscale, Angle):
    """
    La funzione si occupa di calcolare le trasformazioni (scalare 
    ruotare) di un punto le cui coordinate sono passate in input.
    
    Keyword arguments:
    x -- Coordinata x del punto da "trasformare"
    y -- Coordinata y del punto da "trasformare"
    Xscale -- Fattore di scala asse X
    Yscale -- Fattore di scala asse Y
    Angle -- Angolo di rotazione
    """
    global XScale
    global YScale

    xScaled = x * Xscale
    yScaled = y * Yscale
    dist0 = sqrt(pow(xScaled,2) + pow(yScaled,2))
    dirXY = atan2(xScaled, yScaled)
    rotX = dist0 * cos(dirXY + Angle)
    rotY = dist0 * sin(dirXY + Angle)
    # x += rotX
    # y += rotY
    #print '%4f, %4f' %(rotX, rotY)
    return (x+rotX, y+rotY)


def help_message(): #engrave-lines
    print '''engrave-lines.py G-Code Engraving Generator for command-line usage
            (C) ArcEye <2012> 
            based upon code from engrave-11.py
            Copyright (C) <2008>  <Lawrence Glaister> <ve7it at shaw dot ca>'''
            
    print '''engrave-lines.py -X -x -i -Y -y -S -s -Z -D -C -W -M -F -P -p -0 -1 -2 -3 ..............
       Options: 
       -h   Display this help message
       -X   Start X value                       Defaults to 0
       -x   X offset between lines              Defaults to 0
       -i   X indent line list                  String of lines to indent in single quotes
       -Y   Start Y value                       Defaults to 0
       -y   Y offset between lines              Defaults to 0
       -S   X Scale                             Defaults to 1
       -s   Y Scale                             Defaults to 1       
       -Z   Safe Z for moves                    Defaults to 2mm
       -D   Z depth for engraving               Defaults to 0.1mm
       -C   Charactor Space %                   Defaults to 25%
       -W   Word Space %                        Defaults to 100%
       -M   Mirror                              Defaults to 0 (No)
       -F   Flip                                Defaults to 0 (No)
       -P   Preamble g code                     Defaults to "G17 G21 G40 G90 G64 P0.003 F50"
       -p   Postamble g code                    Defaults to "M2"
       -0   Line0 string follow this
       -1   Line1 string follow this
       -2   Line2 string follow this        
       -3   Line3 string follow this
       -4   Line4 string follow this
       -5   Line5 string follow this
       -6   Line6 string follow this
       -7   Line7 string follow this                                
       -8   Line8 string follow this
       -9   Line9 string follow this
      Example
      engrave-lines.py -X7.5 -x5 -i'123' -Y12.75 -y5.25 -S0.4 -s0.5 -Z2 -D0.1 -0'Line0' -1'Line1' -2'Line2' -3'Line3' > test.ngc
    '''
    sys.exit(0)
    
#=======================================================================
# This routine parses the .cxf font file and builds a font dictionary of
# line segment strokes required to cut each character.
# Arcs (only used in some fonts) are converted to a number of line
# segemnts based on the angular length of the arc. Since the idea of
# this font description is to make it support independant x and y scaling,
# we can not use native arcs in the gcode.
#=======================================================================
def parse(file): #engrave-lines
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
            # since font defn has arcs as ccw, we need some font foo
            if ( end_angle < start_angle ):
                start_angle -= 360.0
            # approximate arc with line seg every 20 degrees
            segs = int((end_angle - start_angle) / 20) + 1
            angleincr = (end_angle - start_angle)/segs
            xstart = cos(start_angle * pi/180) * radius + xcenter
            ystart = sin(start_angle * pi/180) * radius + ycenter
            angle = start_angle
            for i in range(segs):
                angle += angleincr
                xend = cos(angle * pi/180) * radius + xcenter
                yend = sin(angle * pi/180) * radius + ycenter
                coords = [xstart,ystart,xend,yend]
                stroke_list += [Line(coords)]
                xmax = max(xmax, coords[0], coords[2])
                ymax = max(ymax, coords[1], coords[3])
                xstart = xend
                ystart = yend
    return font