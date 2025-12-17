#!/usr/bin/env python3
"""
Convenience script to start the Humanoid Robotics RAG Chatbot backend.
This script ensures the backend starts with proper document indexing.
"""
import subprocess
import sys
import os

def main():
    print("Starting Humanoid Robotics RAG Chatbot Backend...")
    print("Ensuring documents are indexed...")

    # Change to the backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)

    # Start the FastAPI server
    print("Starting server on http://localhost:8000")
    try:
        import uvicorn
        from main import app
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except ImportError:
        print("uvicorn not found. Please install it with: pip install uvicorn")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()