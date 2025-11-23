#!/bin/bash

# Expense Tracker - Server Startup Script

echo "=========================================="
echo "  Expense Tracker - Web Server"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if Flask is installed
if ! python3 -c "import flask" &> /dev/null; then
    echo "Flask is not installed. Installing dependencies..."
    pip3 install -r requirements.txt
    echo ""
fi

# Check if app.py exists
if [ ! -f "app.py" ]; then
    echo "Error: app.py not found in current directory"
    exit 1
fi

echo "Starting Flask server..."
echo "Press Ctrl+C to stop the server"
echo ""

# Run the Flask app (app.py will automatically find a free port)
python3 app.py

