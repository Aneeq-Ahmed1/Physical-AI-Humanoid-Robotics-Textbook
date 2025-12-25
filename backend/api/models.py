from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatRequest(BaseModel):
    query: str
    selected_text: Optional[str] = None
    session_id: Optional[str] = None
    language: str = "en"  # Default to English


class ChatResponse(BaseModel):
    answer: str
    citations: List[Dict[str, Any]]
    mode: str  # "full_rag" or "selected_text"
    session_id: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime


class RetrievedDocument(BaseModel):
    text: str
    source_file: str
    chunk_index: int
    similarity_score: float