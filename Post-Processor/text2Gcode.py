#!/usr/bin/python

"""
    engrave-lines.py G-Code Plotting Generator for command-line usage
    (C) ArcEye <2012>  <arceye at mgware dot co dot uk>
    syntax  ---   see helpfile below
    
    Allows the generation of multiple lines of engraved text in one go
    Will take each string arguement, apply X and Y offset generating code until last line done
    
  
    based upon code from engrave-11.py
    Copyright (C) <2008>  <Lawrence Glaister> <ve7it at shaw dot ca>
                     based on work by John Thornton  -- GUI framwork from arcbuddy.py
                     Ben Lipkowitz  (fenn)-- cxf2cnc.py v0.5 font parsing code

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    Rev v2 21.06.2012 ArcEye
"""
# change this if you want to use another font
# fontfile = "/usr/share/qcad/fonts/romanc.cxf"
fontfile = "fonts/italict.cxf"

#from Tkinter import *
from math import *
import os
import re
import string
import getopt

"""
Importo tutte le funzioni definite nella libreria t2gLib
Utilizzando la formula "from / import" non sono costretto a specificare
il nome del modulo t2gLib ad ogni utilizzo.
"""
from t2gLib import *
#from engLineLib import *

String =   ""
SafeZ =    2 					#Altezza del piano di svincolo
XStart =   0 					#Coordinata X di start
XLineOffset =   0
XIndentList = ""
YStart = 0
YLineOffset = 0
Depth =    0.1
XScale =   1
YScale =   1
CSpaceP =  25
WSpaceP= 50
Angle = 0
Mirror = 0
Flip = 0

# Contenuto dell'header del G-Code
Preamble = ["G21 ;Set Units to Millimeters"]
Preamble +=["G90 ;Set to Absolute Positioning"]
Preamble +=["G28 ;Move to Origin (Home)"]
Preamble +=['G0 Z%.4f ;Per compatibilità G-Code viewers'%(Depth)]

# Contenuto footer G-Code
Postamble = ["M2"]

stringlist = []

def __init__(key):
    key = key
    stroke_list = []

def __repr__():
    return "%s" % (stroke_list)

def get_xmax():
    try: return max([s.xmax for s in stroke_list[:]])
    except ValueError: return 0

def get_ymax():
    try: return max([s.ymax for s in stroke_list[:]])
    except ValueError: return 0

                                                                           

#================================================#


def __init__( coords):
    xstart, ystart, xend, yend = coords
    xmax = max(xstart, xend)
    ymax = max(ystart, yend)

def __repr__():
    return "Line([%s, %s, %s, %s])" % (xstart, ystart, xend, yend) 




#================= code ==========================#
def code(arg, lineNumber, last):
   """
   """

   global SafeZ
   global XStart
   global XLineOffset
   global XIndentList
   global YStart
   global YLineOffset
   global Depth
   global XScale
   global YScale
   global CSpaceP
   global WSpaceP
   global Angle
   global Mirror
   global Flip
   global Preamble
   global Postamble
   global stringlist

   String = arg

   #Erase old gcode
   gcode = []

   file = open(fontfile)

   oldx = oldy = -99990.0      

   # Initializing line start coordinates
   XStartLine = XStart
   YStartLine = YStart
   
                 
   if lineNumber != 0:                     #From the second line onward
      gcode.append(";(================================)")
      gcode.append(';Plotting: "%s" ' %(String))
      gcode.append(';Line %d ' %(lineNumber))
      
      # Applying line height if required (-y)
      if YLineOffset:
         YStartLine -= YLineOffset* lineNumber
      
      # Applyng line indentation if required (-x)
      if XLineOffset :
         XStartLine += XLineOffset * lineNumber

      gcode.append(";(================================)")
      
   else: #First line
        gcode.append(";=============================")
        gcode.append('; G-Code generated with Text2G-Code V0.1 ')
        gcode.append('; Created by Salvatore SaXeee Di Benedetto')
        gcode.append('; Based on <Lawrence Glaister> work \"Engrave-lines\" ')
        gcode.append(";=============================")
        gcode.append('; Plotting text: "%s"' %(String) )
        gcode.append('; Fontfile: %s ' %(fontfile))
        gcode.append('; Line %d ' %(lineNumber))
        gcode.append(";=============================")

        gcode.append('; Coordinata di partenza X: %.4f' %(XStartLine))
        gcode.append('; Coordinata di partenza Y: %.4f' %(YStart))
        gcode.append("; Fattore di scala X: %.4f" %(XScale))
        gcode.append("; Fattore di scala X: %.4f" %(YScale))
        gcode.append("; Angolo: %.4f" %(Angle))
        gcode.append(";====================================================")

        # Aggiungo il preambolo al G-Code
        preamble(gcode, Preamble)

   # [ToRework] Do not rebuild the font dictionary for each line to plot
   font = parse(file)          # build stroke lists from font file
   file.close()

   font_line_height = max(font[key].get_ymax() for key in font)
   font_word_space =  max(font[key].get_xmax() for key in font) * (WSpaceP/100.0)
   font_char_space = font_word_space * (CSpaceP /100.0)
   
   #x/y offset 
   xoffset = yoffset = 0
   
   if XStartLine:
      xoffset += XStartLine         # distance along raw string in font units
    
   if YStartLine:
      yoffset += YStartLine

   # calc a plot scale so we can show about first 15 chars of string
   # in the preview window
   PlotScale = 15 * font['A'].get_xmax() * XScale / 150

   for char in String:
        if char == ' ':
            xoffset += font_word_space
            continue
        try:
            gcode.append("; =================")
            gcode.append("; | Plotting character '%s' |" % sanitize(char))
            gcode.append("; =================")
            
            
            first_stroke = True
            # plot each line (stroke) of selected character
            for stroke in font[char].stroke_list:
               
               xSartStroke = stroke.xstart* XScale
               ySartStroke = stroke.ystart*YScale
               
               xEndStroke = stroke.xend* XScale
               yEndStroke = stroke.yend*YScale
               
               dx = oldx - stroke.xstart
               dy = oldy - stroke.ystart
               dist = sqrt(dx*dx + dy*dy)
               oldx, oldy = xEndStroke, yEndStroke

               # Add the offset for the already printed segments at the starting point of the current segment
               xSartStroke += xoffset
               xEndStroke += xoffset
               
               ySartStroke += yoffset
               yEndStroke += yoffset
               
               # check and see if we need to move to a new discontinuous start point
               if (dist > 0.001) or first_stroke:
                  first_stroke = False
                  travel(gcode, xSartStroke, ySartStroke)
               
               
               extQtt = sqrt(pow(stroke.xstart-stroke.xend,2) + pow(stroke.ystart-stroke.yend,2))
               gcode.append('G1 X%.4f Y%.4f E%.4f' %(xEndStroke,yEndStroke,extQtt))
            
            # move over for next character
            char_width = font[char].get_xmax()
            xoffset += font_char_space + (char_width * XScale)

        except KeyError:
           gcode.append("(warning: character '0x%02X' not found in font defn)" % ord(char))

        gcode.append("")       # blank line after every char block

    # finish up with icing
   if last:
        postamble(gcode, Postamble)

   for line in gcode:
            sys.stdout.write(line+'\n')



#================================================

def main():

   debug = 0
   # need to declare the globals because we want to write to them
   # otherwise python will create a local of the same name and
   # not change the global - stupid python
   global SafeZ
   global XStart
   global XLineOffset
   global XIndentList
   global YStart
   global YLineOffset
   global Depth
   global XScale
   global YScale
   global CSpaceP
   global WSpaceP
   global Angle
   global Mirror
   global Flip
   global Preamble
   global Postamble
   global stringlist
   
   try:
      options, xarguments = getopt.getopt(sys.argv[1:], 'hd:X:x:i:Y:y:S:s:Z:D:C:W:M:F:P:p:L:0:1:2:3:4:5:6:7:8:9:')
   except getopt.error:
      print 'Error: You tried to use an unknown option. Try `engrave-lines.py -h\' for more information.'
      sys.exit(0)

   if len(sys.argv[1:]) == 0:
      help_message()
      sys.exit(0)    
    
   for a in options[:]:
      if a[0] == '-h':
         help_message()
         sys.exit(0)

   #  hidden debug option for testing            
   for a in options[:]:
      if a[0] == '-d' and a[1] != '':
         debug = int(a[1])
         print'; DEBUG mode actived' 
         options.remove(a)
         break

   for a in options[:]:
      if a[0] == '-X' and a[1] != '':
         XStart = float(a[1])
         if debug:            
            print'; DEBUG: X = %.4f' %(XStart)
         options.remove(a)
         break

   for a in options[:]:
      if a[0] == '-x' and a[1] != '':
         XLineOffset = float(a[1])
         if debug:
            print'; DEBUG: x = %.4f' %(XLineOffset)
         options.remove(a)
         break

   for a in options[:]:
      if a[0] == '-i' and a[1] != '':
         XIndentList = a[1]
         if debug:
            print'; DEBUG: i = %s' %(a[1])
         options.remove(a)
         break
         
   for a in options[:]:
      if a[0] == '-Y' and a[1] != '':
         YStart = float(a[1])
         if debug:
             print'; DEBUG: Y = %.4f' %(YStart)
         options.remove(a)
         break

   for a in options[:]:
      if a[0] == '-y' and a[1] != '':
         YLineOffset = float(a[1])
         if debug:
            print'; DEBUG: y = %.4f' %(YLineOffset)
         options.remove(a)
         break
            
   for a in options[:]:
      if a[0] == '-S' and a[1] != '':
         XScale = float(a[1])
         if debug:
            print'; DEBUG: S = %.4f' %(XScale)
         options.remove(a)
         break            

   for a in options[:]:
      if a[0] == '-s' and a[1] != '':
         YScale = float(a[1])
         if debug:
            print'; DEBUG: s = %.4f' %(YScale)
         options.remove(a)
         break              

   for a in options[:]:
      if a[0] == '-Z' and a[1] != '':
         SafeZ = float(a[1])
         if debug:
            print'; DEBUG: Z = %.4f' %(SafeZ)
         options.remove(a)
         break  
  
   for a in options[:]:
      if a[0] == '-D' and a[1] != '':
         Depth = float(a[1])
         if debug:
            print'; DEBUG: D = %.4f' %(Depth)
         options.remove(a)
         break    
  
   for a in options[:]:
      if a[0] == '-C' and a[1] != '':
         CSpaceP = float(a[1])
         if debug:
            print'; DEBUG: C = %.4f' %(CSpaceP)
         options.remove(a)
         break      

   for a in options[:]:
      if a[0] == '-W' and a[1] != '':
         WSpaceP = float(a[1])    
         if debug:
            print'; DEBUG: W = %.4f' %(WSpaceP)
         options.remove(a)
         break      

   for a in options[:]:
      if a[0] == '-A' and a[1] != '':
         Angle = float(a[1])
         if debug:
            print'; DEBUG: A = %.4f' %(Angle)
         options.remove(a)
         break  


   for a in options[:]:
      if a[0] == '-M' and a[1] != '':
         Mirror = float(a[1])
         if debug:
            print'; DEBUG: M = %.4f' %(Mirror)
         options.remove(a)
         break  

   for a in options[:]:
      if a[0] == '-F' and a[1] != '':
         Flip = float(a[1])
         if debug:
            print'; DEBUG: F = %.4f' %(Flip)
         options.remove(a)
         break  

   for a in options[:]:
      if a[0] == '-P' and a[1] != '':
         Preamble = a[1]
         if debug:
            print'; DEBUG: P = %s' %(a[1])
         options.remove(a)
         break  

   for a in options[:]:
      if a[0] == '-p' and a[1] != '':            
         Postamble = a[1]
         if debug:
            print'; DEBUG: p = %s' %(a[1])
         options.remove(a)
         break  

   for a in options[:]:
      if a[0] == '-0' and a[1] != '':
         stringlist.append(a[1])
         if debug:
            print'; DEBUG: 0 = %s' %(a[1])
         options.remove(a)
         break  
            
   for a in options[:]:
      if a[0] == '-1' and a[1] != '':
         stringlist.append(a[1])
         if debug:
            print'; DEBUG: 1 = %s' %(a[1])
         options.remove(a)
         break  
            
   for a in options[:]:
      if a[0] == '-2' and a[1] != '':
         stringlist.append(a[1])
         if debug:
            print'; DEBUG: 2 = %s' %(a[1])
         options.remove(a)
         break  

   for a in options[:]:
      if a[0] == '-3' and a[1] != '':
         stringlist.append(a[1])
         if debug:
            print'; DEBUG: 3 = %s' %(a[1])
         options.remove(a)
         break  
            
   for a in options[:]:
      if a[0] == '-4' and a[1] != '':
         stringlist.append(a[1])
         if debug:
            print'; DEBUG: 4 = %s' %(a[1])
         options.remove(a)
         break  

   for a in options[:]:
      if a[0] == '-5' and a[1] != '':
         stringlist.append(a[1])
         if debug:
            print'; DEBUG: 5 = %s' %(a[1])
         options.remove(a)
         break  

   for a in options[:]:
      if a[0] == '-6' and a[1] != '':
         stringlist.append(a[1])
         if debug:
            print'; DEBUG: 6 = %s' %(a[1])
         options.remove(a)
         break  

   for a in options[:]:
      if a[0] == '-7' and a[1] != '':
         stringlist.append(a[1])
         if debug:
            print'; DEBUG: 7 = %s' %(a[1])
         options.remove(a)
         break  

   for a in options[:]:
      if a[0] == '-8' and a[1] != '':
         stringlist.append(a[1])
         if debug:
            print'; DEBUG: 8 = %s' %(a[1])
         options.remove(a)
         break  

   for a in options[:]:
      if a[0] == '-9' and a[1] != '':
         stringlist.append(a[1])
         if debug:
            print'; DEBUG: 9 = %s' %(a[1])
         options.remove(a)
         break  
            
   for index, item in enumerate(stringlist):
      code(item,index, index == (len(stringlist) - 1) )


#================================================

if __name__ == "__main__":
        main()

#=======================END======================
