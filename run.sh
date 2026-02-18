#!/bin/bash

echo "Starting Network Monitoring Dashboard..."
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the application
echo
echo "Starting Flask application..."
echo "Dashboard will be available at: http://localhost:5000"
echo
echo "Default login credentials:"
echo "Username: admin"
echo "Password: admin123"
echo
echo "Press Ctrl+C to stop the server"
echo

python app.py
