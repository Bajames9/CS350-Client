#!/bin/bash
echo "=== Setting up Python virtual environment ==="

# Create venv if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo
echo "=== Starting client ==="
python3 src/app.py
echo
