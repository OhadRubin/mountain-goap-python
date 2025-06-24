THIS SHOULD BE A LINTER ERROR#!/bin/bash

# Setup script for Mountain GOAP Python
set -e

echo "Setting up Mountain GOAP Python..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv || {
        echo "Failed to create venv. Trying to install python3-venv..."
        sudo apt update && sudo apt install -y python3-venv python3-full
        python3 -m venv venv
    }
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install system dependencies for pygame if needed
echo "Setting up display environment for pygame..."
export SDL_VIDEODRIVER=dummy
export DISPLAY=:99

echo "Setup complete!"
echo ""
echo "To run the RPG example:"
echo "  source venv/bin/activate"
echo "  python -m rpg_goap_python_example.example"
echo ""
echo "Or use the run script:"
echo "  ./run.sh"