@echo off
rem Start the Humanoid Robotics RAG Chatbot backend server
rem Usage: start_backend.bat

echo Starting Humanoid Robotics RAG Chatbot backend server...

cd /d "%~dp0"

rem Set the Python path to include the current directory
set PYTHONPATH=%~dp0

rem Start the uvicorn server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

if errorlevel 1 (
    echo.
    echo Server failed to start. Possible issues:
    echo 1. Make sure you're in the backend directory
    echo 2. Check that all dependencies are installed (pip install -r requirements.txt)
    echo 3. Verify your .env file has the required API keys
    echo 4. Make sure port 8000 is not already in use
    pause
)