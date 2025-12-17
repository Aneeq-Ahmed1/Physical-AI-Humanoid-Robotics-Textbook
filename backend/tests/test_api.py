import asyncio
import aiohttp
import pytest
from fastapi.testclient import TestClient

def get_test_client():
    """Create a test client for the app"""
    from main import app
    return TestClient(app)

def test_health_endpoint():
    """Test the health endpoint"""
    client = get_test_client()
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_chat_endpoint_basic():
    """Test the chat endpoint with a basic query"""
    client = get_test_client()
    # Test full-book RAG mode (without selected text)
    response = client.post("/api/chat", json={
        "query": "What is this textbook about?",
        "selected_text": None,
        "session_id": None
    })

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "citations" in data
    assert "mode" in data
    assert "session_id" in data
    assert data["mode"] in ["full_rag", "selected_text"]

def test_chat_endpoint_selected_text():
    """Test the chat endpoint with selected text mode"""
    client = get_test_client()
    selected_text = "Humanoid robotics is a field that combines robotics and artificial intelligence."

    response = client.post("/api/chat", json={
        "query": "What is humanoid robotics?",
        "selected_text": selected_text,
        "session_id": None
    })

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "citations" in data
    assert "mode" in data
    assert "session_id" in data
    assert data["mode"] == "selected_text"

def test_chat_endpoint_empty_query():
    """Test the chat endpoint with an empty query (should return error)"""
    client = get_test_client()
    response = client.post("/api/chat", json={
        "query": "",
        "selected_text": None,
        "session_id": None
    })

    assert response.status_code == 400

if __name__ == "__main__":
    # Run the tests
    test_health_endpoint()
    print("✓ Health endpoint test passed")

    test_chat_endpoint_basic()
    print("✓ Chat endpoint basic test passed")

    test_chat_endpoint_selected_text()
    print("✓ Chat endpoint selected text test passed")

    test_chat_endpoint_empty_query()
    print("✓ Chat endpoint empty query test passed")

    print("\nAll tests passed! 🎉")