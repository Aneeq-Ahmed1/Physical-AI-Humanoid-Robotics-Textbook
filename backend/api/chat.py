from fastapi import APIRouter, HTTPException
from api.models import ChatRequest, ChatResponse
from vector.qdrant_client import QdrantVectorDB
from agent.llm_agent import LLMAgent
from db.session_manager import SessionManager
from typing import Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chat_router = APIRouter()
vector_db = QdrantVectorDB()
llm_agent = LLMAgent()
session_manager = SessionManager()

@chat_router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Validate request
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        # Get or create session
        session_id = request.session_id
        if not session_id:
            session_id = session_manager.create_session()
        else:
            # Verify session exists and is not expired
            session = session_manager.get_session(session_id)
            if not session:
                session_id = session_manager.create_session()

        # Determine mode and generate response
        if request.selected_text:
            # Selected-text mode: answer only from the selected text
            logger.info(f"Processing in selected-text mode for session {session_id}")

            # Limit selected text to first 500 words/characters as per requirements
            limited_selected_text = request.selected_text[:500] if len(request.selected_text) > 500 else request.selected_text

            response = llm_agent.generate_response_selected_text(
                query=request.query,
                selected_text=limited_selected_text
            )

            result = ChatResponse(
                answer=response,
                citations=[],
                mode="selected_text",
                session_id=session_id
            )
        else:
            # Full-book RAG mode: retrieve from Qdrant and generate response
            logger.info(f"Processing in full-book RAG mode for session {session_id}")

            # Create embedding for the query
            query_embedding = vector_db.embed_text(request.query)

            # Retrieve relevant documents from Qdrant
            retrieved_docs = vector_db.search(query_vector=query_embedding, top_k=3)

            # Generate response using the LLM agent
            response = llm_agent.generate_response_full_rag(
                query=request.query,
                context_documents=retrieved_docs
            )

            # Format citations
            citations = [
                {
                    "source": doc["source_file"],
                    "chunk_index": doc["chunk_index"],
                    "similarity_score": doc["similarity_score"]
                }
                for doc in retrieved_docs
            ]

            result = ChatResponse(
                answer=response,
                citations=citations,
                mode="full_rag",
                session_id=session_id
            )

        # Save user message and assistant response to session history
        session_manager.save_message(
            session_id=session_id,
            role="user",
            content=request.query,
            selected_text=request.selected_text
        )

        session_manager.save_message(
            session_id=session_id,
            role="assistant",
            content=result.answer,
            citations=result.citations
        )

        # Add session_id to response for frontend tracking
        # Note: The response model doesn't include session_id, but we could extend it if needed
        return result

    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")