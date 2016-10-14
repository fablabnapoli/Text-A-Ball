@echo off

REM Insert here your python path
set python=%~d0%\winPenPack\Bin\Python2\python.exe

set curDir=%~dp0%

REM Starting tweet grabber
REM start "TaB Tweet Grabber" /B /D %curDir%\ "%python%" ".\bin\tweet2DB.py"

REM Starting web UI
start "TaB Web UI" /B /D %curDir%\ "%python%" ".\bin\webUI.py"

REM Starting printers listner
REM start "TaB Web UI" /B /D %curDir%\ "%python%" ".\bin\webUI.py"