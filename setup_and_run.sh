#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed."
    exit
fi

# Create a virtual environment
echo "Creating a virtual environment..."
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Launch the game
echo "Launching the game..."
echo "Credits : PouchyCorp, Tioh, Ytyt, Leih"
python main.py

# Deactivate the environment
deactivate
