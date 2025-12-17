# Humanoid Robotics Textbook with Embedded Agentic RAG Chatbot

This project implements an intelligent chatbot for the Humanoid Robotics textbook using an agentic RAG (Retrieval-Augmented Generation) approach. The system combines Cohere's Command-R model with Qdrant vector database to provide contextually aware responses.

## Features

### 1. Full-Book RAG Mode
- Retrieves relevant content from the entire textbook using vector search
- Uses Cohere embeddings for semantic similarity
- Provides citations to source material
- Maintains conversational context

### 2. Selected-Text Mode
- Answers questions based only on user-selected text
- Prevents context leakage from other parts of the book
- Automatically detects text selection on the page
- Switches to focused mode when text is highlighted

### 3. Session Management
- Maintains conversation history with 24-hour expiration
- SQLite database for session and message storage
- Session continuity across page refreshes

## Architecture

### Backend (FastAPI)
- **API Layer**: FastAPI with proper request/response models
- **LLM Agent**: Cohere Command-R model with tool calling
- **Vector DB**: Qdrant for document retrieval
- **Session Management**: SQLite for conversation history
- **Error Handling**: Comprehensive error handling and logging

### Frontend (Docusaurus)
- **Chat Widget**: Persistent, floating chat interface
- **Text Selection Detection**: Automatic detection of selected text
- **Responsive Design**: Works on desktop and mobile
- **Real-time Interaction**: Instant messaging with typing indicators

## Project Structure

```
backend/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── api/                    # API routes and models
│   ├── models.py          # Pydantic models
│   ├── chat.py            # Chat endpoint implementation
│   └── health.py          # Health check endpoint
├── agent/                 # LLM agent implementation
│   └── llm_agent.py       # Cohere-based agent
├── db/                    # Database operations
│   └── session_manager.py # Session and message management
├── vector/                # Vector database operations
│   └── qdrant_client.py   # Qdrant vector database client
└── tests/                 # Integration tests
    └── integration_test.py # System integration tests

my-website/
├── src/
│   └── components/
│       └── ChatWidget/    # Chat widget React components
│           ├── ChatWidget.jsx
│           ├── ChatWidget.css
│           └── index.js
└── src/theme/
    └── Root.js           # Docusaurus root wrapper
```

## Setup and Installation

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys and connection strings
   ```

4. Required environment variables:
   - `COHERE_API_KEY`: Your Cohere API key
   - `QDRANT_URL`: Your Qdrant cluster URL
   - `QDRANT_API_KEY`: Your Qdrant API key

5. Start the backend server:
   ```bash
   # From the backend directory
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   If you encounter import issues, use:
   ```bash
   PYTHONPATH=. uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   Or use the provided startup scripts:
   - Windows: `start_backend.bat`
   - Linux/Mac: `./start_backend.sh`

### Frontend Setup
1. Navigate to the website directory:
   ```bash
   cd my-website
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure the API URL (optional - defaults to http://localhost:8000):
   ```bash
   # Set environment variable before starting
   export CHATBOT_API_URL=http://your-backend-url:8000
   # Then start the development server:
   npm run start
   ```

4. Start the development server:
   ```bash
   npm run start
   ```

   Note: If you're using Windows Command Prompt, use:
   ```cmd
   set CHATBOT_API_URL=http://your-backend-url:8000 && npm run start
   ```

## API Endpoints

### POST `/api/chat`
Main chat endpoint that handles both full-book RAG and selected-text modes.

**Request Body:**
```json
{
  "query": "string",
  "selected_text": "string | null",
  "session_id": "string | null"
}
```

**Response:**
```json
{
  "answer": "string",
  "citations": [],
  "mode": "full_rag | selected_text",
  "session_id": "string"
}
```

### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "datetime"
}
```

## Frontend Integration

The chat widget is automatically integrated into all pages via the Docusaurus Root component. The widget includes:

- Persistent floating interface
- Text selection detection
- Session management
- Responsive design
- Typing indicators
- Citation display

## Testing

Run the integration tests to verify the system:
```bash
cd backend
python tests/integration_test.py
```

## Deployment

### Backend
- Deploy on Render free tier or similar platform
- Ensure environment variables are set in deployment environment
- Configure Qdrant and Cohere API access

### Frontend
- Deploy to GitHub Pages using Docusaurus build process
- The chat widget will automatically connect to your backend API

## Development Notes

- The Cohere Generate API has been deprecated; the system handles this gracefully
- Qdrant collection must exist for full-book RAG functionality
- Session data is stored in SQLite (sessions.db)
- The frontend automatically detects text selection and switches modes

## License

This project is part of the Humanoid Robotics Textbook initiative.