# Tweet - A - Ball

## Project description.
Tweet A Ball (TaB) is a robot designed to "draw" the text of tweets containing specific hashtags on balls, eggs and other spherical surfaces.

Unlike other Eggbot and similar, TaB is fully autonomous and does not require an external control station (PC) or software for processing text draw.

## Project history.
TaB was designed by Fablab Naples within IntelMaker competition for the occasion of Maker Faire 2016 exhibition.

The project, mainly intended for teaching purposes, aims to explore Intel Edison platform capability.

## How does TaB works?.
Exploiting the power of Intel Edison, TaB can connect directly to internet and scan the Twitter stream to research specific topics of discussion (hashtags).

Identified a message matching the search criteria, the software inside the robot converts the text in lines, curves and points.

Finally the whole is converted into a sequence of movement commands that trigger the writing arm.

## Software stack.
The entire software stack is designed specifically for the Intel Edison platform and consists of the following modules:

* Dispatcher
* Host
* Post-processor
* Firmware

The modules * Dispatcher *, * Host * and * Post-processors * have been designed in Python and are executed by Intel Edison CPU, while the firmware module has been adapted for Intel Edison MCU.

### Dispatcher.
It is the module that deals with the selection and filtering of tweets and spool management (print queue).

### Host.
He receives the text from the dispatcher, sends it to the post-processor to convert into machine instructions (G-Code) and oversee to the execution by sending to the Firmware one instruction at a time.

### Post-processor.
It translates the text supplied to the Host in a sequence of lines, curves and points. Then converts these in motion instructions (G-Code commands).

### Firmware.
It is the core of the entire system, it converts the G-code instructions into electrical impulses to the motors, and then in motion of the print cursor and of the ball itself.

## TAB Network.
The internal software stack has been designed to allow more TaB robots work together in the tweet representation.

That is, a "*network of TaB robots*".

In this configuration one of TaB assumes the role of master, taking charge of selecting the tweets to draw and the other acting as a slave waiting by the first content to be displayed.

A multi-TaB configuration has only one active Dispatcher module at a time that communicates via WiFi with different Host modules.

This configuration allows you to *draw multiple tweets* at a time.

<!--
## Hardware stack
-->