@echo off
echo Starting Humanoid Robotics RAG Chatbot Backend with Document Indexing...

REM Change to the backend directory
cd /d "%~dp0"

REM Install dependencies if not already installed
echo Installing dependencies...
pip install -r requirements.txt

REM Start the backend server with auto-document indexing
echo Starting backend server...
python -c "from main import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8000)"