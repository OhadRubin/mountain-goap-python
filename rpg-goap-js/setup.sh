#!/bin/bash

# Setup script for RPG GOAP JavaScript
set -e

echo "Setting up RPG GOAP JavaScript..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js not found. Please install Node.js first."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "Error: npm not found. Please install npm first."
    exit 1
fi

echo "Node.js version: $(node --version)"
echo "npm version: $(npm --version)"

# Install dependencies
echo "Installing dependencies..."
npm install

echo "Setup complete!"
echo ""
echo "To run the RPG example:"
echo "  ./run.sh"
echo ""
echo "To test the example:"
echo "  timeout 10 npm start"
echo ""
echo "To run tests:"
echo "  npm test"