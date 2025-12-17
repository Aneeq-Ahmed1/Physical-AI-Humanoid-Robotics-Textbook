# Tests

This directory contains tests for the Humanoid Robotics RAG Chatbot backend.

## Running Tests

To run the tests, make sure you have the required dependencies installed:

```bash
pip install pytest
```

Then run the tests:

```bash
# Run all tests
python -m pytest tests/

# Run tests with verbose output
python -m pytest tests/ -v

# Run the test script directly
python tests/test_api.py
```

## Test Structure

- `test_api.py`: Contains API endpoint tests using FastAPI's TestClient
- More test files can be added as the project grows

## Test Coverage

The tests currently cover:

- Health endpoint functionality
- Chat endpoint in full-book RAG mode
- Chat endpoint in selected-text mode
- Error handling for empty queries
- Session ID management
- Response structure validation