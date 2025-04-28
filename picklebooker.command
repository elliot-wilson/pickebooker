#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
python3 picklebooker.py

# if you'd like to move this command file to a different location, drag and drop it to the location of your choice
# then update line 2 with the path to the Picklebooker directory, e.g.:
# cd ~/Documents/picklebooker