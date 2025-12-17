# Humanoid Robotics RAG Chatbot Backend

This is the backend service for the Humanoid Robotics textbook's embedded RAG chatbot. It provides intelligent question-answering capabilities using retrieval-augmented generation (RAG) and supports both full-book and selected-text modes.

## Architecture

The backend is built with the following components:

- **FastAPI**: Web framework for building the API
- **Google Gemini**: LLM service for natural language processing via OpenAI SDK wrapper
- **Qdrant**: Vector database for storing and retrieving book content
- **Neon Postgres**: Serverless database for session and chat history management

## Features

1. **Full-book RAG Mode**: Answers questions by retrieving relevant content from the entire book
2. **Selected-text Mode**: Answers questions based only on user-selected text, preventing context leakage
3. **Session Management**: Maintains conversation history with 24-hour expiration
4. **Citation Tracking**: Provides source citations for RAG responses

## Directory Structure

```
backend/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── api/                   # API routes and models
│   ├── models.py          # Pydantic models
│   ├── chat.py            # Chat endpoint implementation
│   └── health.py          # Health check endpoint
├── agent/                 # LLM agent implementation
│   ├── llm_agent.py       # Gemini-based agent
│   └── gemini_openai_wrapper.py  # OpenAI SDK wrapper for Gemini
├── db/                    # Database operations
│   └── session_manager.py # Session and message management
└── vector/                # Vector database operations
    └── qdrant_client.py   # Qdrant vector database client
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your actual API keys and connection strings
```

3. Run the application:
```bash
uvicorn main:app --reload
```

### Auto-Document Indexing
On startup, the application will automatically:
- Check if the Qdrant vector database has indexed documents
- If no documents exist, it will read all markdown files from `../my-website/docs`
- Chunk and index the documentation content for RAG functionality
- Log the number of documents indexed

This ensures that the full-book RAG mode has content to search from the Humanoid Robotics textbook.

## API Endpoints

- `POST /api/chat`: Main chat endpoint
  - Request: `{"query": "string", "selected_text": "string | null", "session_id": "string"}`
  - Response: `{"answer": "string", "citations": [], "mode": "full_rag | selected_text"}`

- `GET /health`: Health check endpoint
  - Response: `{"status": "healthy", "timestamp": "datetime"}`

## Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key for LLM and embeddings
  - Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
- `QDRANT_URL`: Your Qdrant cluster URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `NEON_DB_URL`: Your Neon Postgres connection string

## Deployment

The backend is designed to work on free-tier services:
- Qdrant Cloud Free Tier
- Neon Serverless Postgres
- Deployable on Render free tier

## Frontend Integration

The backend is designed to work with the Docusaurus-based textbook website. The frontend should:
1. Detect text selection using browser APIs
2. Send selected text along with queries when text is highlighted
3. Display a UI indicator when in selected-text mode
4. Maintain session ID for conversation continuity