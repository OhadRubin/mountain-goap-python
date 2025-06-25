#!/bin/bash

# Run script for RPG GOAP JavaScript Example
set -e

echo "Running RPG GOAP JavaScript Example..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js not found. Please run ./setup.sh first."
    exit 1
fi

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "Dependencies not found. Running setup..."
    ./setup.sh
fi

# Run the example with timeout
timeout 10 npm start