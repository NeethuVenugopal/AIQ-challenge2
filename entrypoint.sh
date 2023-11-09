#!/bin/bash

# Get the current directory
SCRIPT_DIR="$(pwd)"

# Execute a script in the same directory
python "$SCRIPT_DIR/readandsave.py"

python "$SCRIPT_DIR/app.py" 