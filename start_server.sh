#!/bin/bash
# Start Rock Paper Scissors Flask Server

cd "$(dirname "$0")"

echo "🚀 Starting Rock Paper Scissors Server..."

# Activate virtual environment
source venv/bin/activate

# Start Flask server
python app.py

echo "Server stopped."

