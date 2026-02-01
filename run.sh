#!/bin/bash

# Shell script to run the Command Chat Assistant

echo "Command Chat Assistant - Setup and Run"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error creating virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error installing dependencies"
    exit 1
fi

echo ""
echo "Starting Command Chat Assistant..."
echo ""

# Run the application
python command_chat_app.py
