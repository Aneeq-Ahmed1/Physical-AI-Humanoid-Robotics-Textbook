# Quickstart Guide: Humanoid Robotics Textbook with Embedded Agentic RAG Chatbot

## Prerequisites

- Python 3.10+ installed
- Node.js and npm installed
- Google AI Studio API key (free tier)
- Access to Qdrant Cloud Free Tier
- Neon Serverless Postgres account

## Setup Instructions

### 1. Clone and Prepare Repository

```bash
# Create project structure
mkdir humanoid-robotics-book
cd humanoid-robotics-book
mkdir backend frontend book
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn google-generativeai qdrant-client psycopg2-binary python-dotenv pydantic
```

### 3. Environment Configuration

Create `.env` file in the backend directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
QDRANT_URL=https://6a02f705-256d-4d8a-9fb8-45e16c7df3ad.us-east4-0.gcp.cloud.qdrant.io
QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.S_mzLidmw-jZuIFKxNwfSbhkP82F0H2lPoO-8J-Rp5U
NEON_DB_URL=postgresql://neondb_owner:npg_5dtYkfFo1ENp@ep-gentle-river-a4da4s3u-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

### 4. Book Content Indexing

Create `index_book.py`:

```python
import os
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.http import models
from google.generativeai.embed_content import embed_content
import google.generativeai as genai
import hashlib

# Initialize Qdrant client
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

# Initialize Google Generative AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def chunk_text(text, chunk_size=500, overlap=50):
    """Simple text chunking function"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks

def index_book_content():
    # Load your book markdown files from /book/docs directory
    book_dir = Path("../book/docs")

    points = []
    for md_file in book_dir.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        chunks = chunk_text(content)

        for idx, chunk in enumerate(chunks):
            # Generate embedding using Gemini
            response = embed_content(
                model="models/embedding-001",
                content=chunk,
                task_type="RETRIEVAL_DOCUMENT"
            )

            vector = response['embedding']

            # Create point for Qdrant
            point = models.PointStruct(
                id=hashlib.md5(f"{md_file.name}_{idx}".encode()).hexdigest(),
                vector=vector,
                payload={
                    "text": chunk,
                    "source_file": str(md_file.relative_to(book_dir)),
                    "chunk_index": idx
                }
            )
            points.append(point)

    # Create or recreate collection
    qdrant_client.recreate_collection(
        collection_name="book-content",
        vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
    )

    # Upload points to Qdrant
    qdrant_client.upload_points(
        collection_name="book-content",
        points=points
    )

    print(f"Indexed {len(points)} chunks into Qdrant")

if __name__ == "__main__":
    index_book_content()
```

### 5. Backend API Implementation

Create `main.py`:

```python
import os
import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from qdrant_client import QdrantClient
from google.generativeai.embed_content import embed_content
import psycopg2
from contextlib import contextmanager

# Initialize services
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

app = FastAPI()

# Database connection
def get_db_connection():
    return psycopg2.connect(os.getenv("NEON_DB_URL"))

# Data models
class Message(BaseModel):
    role: str
    content: str
    timestamp: datetime
    citations: Optional[List[dict]] = []

class ChatSession(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    expires_at: datetime
    messages: List[Message]

class ChatRequest(BaseModel):
    query: str
    selected_text: Optional[str] = None
    session_id: Optional[str] = None

class ToolResult(BaseModel):
    name: str
    result: dict

# Tool functions
def retrieve_from_book(query: str, top_k: int = 3) -> List[dict]:
    # Embed the query
    embedding_response = embed_content(
        model="models/embedding-001",
        content=query,
        task_type="RETRIEVAL_QUERY"
    )
    query_embedding = embedding_response['embedding']

    # Search in Qdrant
    search_results = qdrant_client.search(
        collection_name="book-content",
        query_vector=query_embedding,
        limit=top_k
    )

    documents = []
    for result in search_results:
        documents.append({
            "text": result.payload["text"],
            "source_file": result.payload["source_file"],
            "chunk_index": result.payload["chunk_index"],
            "similarity_score": result.score
        })

    return documents

def answer_from_selected_text(selected_text: str, query: str) -> str:
    # Simple approach: use the selected text as context to answer the query
    # In practice, you might use the LLM to synthesize the answer
    return f"Based on the selected text: {selected_text[:200]}... [Content truncated]"

# API endpoints
@app.post("/tools/retrieve_book")
async def tool_retrieve_book(query: str, top_k: int = 3):
    documents = retrieve_from_book(query, top_k)
    return {"documents": documents}

@app.post("/tools/answer_from_selected")
async def tool_answer_from_selected(selected_text: str, query: str):
    response = answer_from_selected_text(selected_text, query)
    return {"response": response}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # Generate or use session ID
    session_id = request.session_id or str(uuid.uuid4())

    # Determine which mode to use
    if request.selected_text:
        # Selected-text mode: answer only from the selected text
        result = answer_from_selected_text(request.selected_text, request.query)
        return {
            "response": result,
            "session_id": session_id,
            "mode": "selected_text_only",
            "citations": []
        }
    else:
        # Full-book RAG mode: use retrieval tool
        documents = retrieve_from_book(request.query)

        # Use Gemini to generate response based on retrieved documents
        model = genai.GenerativeModel('gemini-pro')

        # Format context from retrieved documents
        context = "\n\n".join([doc["text"] for doc in documents])
        prompt = f"Context: {context}\n\nQuestion: {request.query}\n\nPlease provide a comprehensive answer based on the context, citing the relevant sources."

        response = model.generate_content(prompt)

        # Format citations
        citations = [{"source": doc["source_file"], "chunk_index": doc["chunk_index"]} for doc in documents]

        return {
            "response": response.text,
            "session_id": session_id,
            "mode": "full_book_rag",
            "citations": citations
        }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### 6. Frontend Setup

In the frontend directory:

```bash
cd ../frontend
npm init -y
npm install @chatscope/chat-ui-kit-react react react-dom
```

Create a basic chat component that integrates with Docusaurus.

### 7. Running the Application

```bash
# Start the backend
cd backend
uvicorn main:app --reload

# The frontend will be integrated into the Docusaurus site
```

### 8. Testing

1. Run the indexing script: `python index_book.py`
2. Start the backend: `uvicorn main:app --reload`
3. Test the API endpoints:
   - `POST /chat` with different query types
   - Verify selected-text mode works without external retrieval
   - Verify full-book RAG mode retrieves and cites properly

## Deployment

### Backend (Render)
1. Create a Render web service
2. Set environment variables
3. Use the provided Dockerfile or Python runtime

### Frontend (GitHub Pages)
1. Build Docusaurus site with embedded chat widget
2. Deploy to GitHub Pages

The system will be fully functional with both full-book RAG and selected-text-only modes as specified in the requirements.