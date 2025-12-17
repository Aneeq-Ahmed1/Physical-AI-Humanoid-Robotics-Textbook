#!/bin/bash
# Start the Humanoid Robotics RAG Chatbot backend server
# Usage: ./start_backend.sh

echo "Starting Humanoid Robotics RAG Chatbot backend server..."

# Change to the script's directory
cd "$(dirname "$0")"

# Set the Python path to include the current directory
export PYTHONPATH="."

# Start the uvicorn server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

if [ $? -ne 0 ]; then
    echo
    echo "Server failed to start. Possible issues:"
    echo "1. Make sure you're in the backend directory"
    echo "2. Check that all dependencies are installed (pip install -r requirements.txt)"
    echo "3. Verify your .env file has the required API keys"
    echo "4. Make sure port 8000 is not already in use"
fi