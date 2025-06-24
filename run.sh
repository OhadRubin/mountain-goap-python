#!/bin/bash

# Run script for Mountain GOAP Python RPG Example
set -e

echo "Running Mountain GOAP Python RPG Example..."

# Set up headless display for pygame
export SDL_VIDEODRIVER=dummy
export DISPLAY=:99

# Try to activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Run the example with timeout
timeout 10 python3 -m rpg_goap_python_example.example