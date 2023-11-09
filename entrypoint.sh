#!/bin/bash

# Get the current directory
SCRIPT_DIR="$(pwd)"

# Execute a script in the same directory
python "$SCRIPT_DIR/readandsave.py" # Function to read and save image in db

python "$SCRIPT_DIR/app.py" # Function to retrieve stored images