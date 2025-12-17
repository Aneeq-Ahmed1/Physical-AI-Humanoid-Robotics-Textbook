"""
Script to run tests and verify the system is working properly.
"""
import subprocess
import sys
import os
from threading import Thread
import time
import requests

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    print("Dependencies installed successfully!")

def run_tests():
    """Run the test suite"""
    print("Running tests...")
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], check=True)
    return result.returncode == 0

def run_test_script():
    """Run the simple test script"""
    print("Running simple test script...")
    result = subprocess.run([sys.executable, "tests/test_api.py"], check=True)
    return result.returncode == 0

if __name__ == "__main__":
    print("Starting system verification...")

    # Install dependencies
    install_dependencies()

    # Run tests
    try:
        run_test_script()
        print("✓ Simple tests passed!")

        # Only run pytest if it's available
        try:
            import pytest
            run_tests()
            print("✓ Pytest tests passed!")
        except ImportError:
            print("⚠ Pytest not available, skipping advanced tests")

        print("\n🎉 All tests completed successfully!")
        print("\nSystem is ready for use!")
        print("To start the backend server, run: uvicorn main:app --reload")

    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed with error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)