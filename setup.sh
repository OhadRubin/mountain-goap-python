#!/bin/bash

# Setup script for Mountain GOAP Python
set -e

echo "Setting up Mountain GOAP Python..."

# Function to install with pip
install_dependencies() {
    echo "Installing pygame..."
    if command -v pip3 &> /dev/null; then
        pip3 install --break-system-packages pygame>=2.0.0 2>/dev/null || pip3 install pygame>=2.0.0
    elif command -v pip &> /dev/null; then
        pip install --break-system-packages pygame>=2.0.0 2>/dev/null || pip install pygame>=2.0.0
    else
        echo "Error: Neither pip nor pip3 found. Please install Python pip first."
        exit 1
    fi
}

# Try to create virtual environment first
echo "Trying to create virtual environment..."
if python3 -m venv venv 2>/dev/null; then
    echo "Virtual environment created successfully."
    source venv/bin/activate
    pip install --upgrade pip
    pip install pygame>=2.0.0
    echo "Dependencies installed in virtual environment."
else
    echo "Virtual environment creation failed. Installing system-wide..."
    install_dependencies
fi

echo "Setup complete!"
echo ""
echo "To run the RPG example:"
echo "  ./run.sh"
echo ""
echo "To test the example:"
echo "  timeout 10 python3 -m rpg_goap_python_example.example"