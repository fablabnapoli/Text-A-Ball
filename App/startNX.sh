#!/bin/bash

# Starting web UI
python ./bin/webUI.py &

# Starting tweet grabber
python ./bin/tweet2DB.py &
