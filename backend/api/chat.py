from fastapi import APIRouter, HTTPException
from .models import ChatRequest, ChatResponse
import sys
import os

# Add the backend directory to Python path to handle relative imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vector.qdrant_client import QdrantVectorDB
from agent.llm_agent import LLMAgent
from agent.agent_router import get_router
from agent.base_agent import AgentRequest
from agent.translation_agent import TranslationAgent
from db.session_manager import SessionManager
from typing import Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chat_router = APIRouter()
vector_db = QdrantVectorDB()
llm_agent = LLMAgent()
translation_agent = TranslationAgent()
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

        # Determine if translation is needed
        target_language = request.language
        needs_translation = target_language.lower() != "en"

        # If translation is needed, translate the query to English for processing
        processed_query = request.query
        processed_selected_text = request.selected_text

        if needs_translation:
            try:
                # Translate query from target language to English for processing
                processed_query = translation_agent.translate_text(
                    request.query,
                    "en",  # Translate to English for processing
                    target_language  # From the user's language
                )

                # If selected text exists, translate it too
                if request.selected_text:
                    processed_selected_text = translation_agent.translate_text(
                        request.selected_text,
                        "en",  # Translate to English for processing
                        target_language  # From the user's language
                    )
            except Exception as e:
                logger.warning(f"Translation failed, proceeding with original query: {str(e)}")
                # If translation fails, proceed with original text

        # Determine mode and generate response
        if processed_selected_text:
            # Selected-text mode: answer only from the selected text
            logger.info(f"Processing in selected-text mode for session {session_id}")

            # Limit selected text to first 500 words/characters as per requirements
            limited_selected_text = processed_selected_text[:500] if len(processed_selected_text) > 500 else processed_selected_text

            response = llm_agent.generate_response_selected_text(
                query=processed_query,
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
            query_embedding = vector_db.embed_text(processed_query)

            # Retrieve relevant documents from Qdrant
            retrieved_docs = vector_db.search(query_vector=query_embedding, top_k=3)

            # Generate response using the LLM agent with English documents
            response = llm_agent.generate_response_full_rag(
                query=processed_query,
                context_documents=retrieved_docs
            )

            # Format citations (keep original source info in English)
            citations = [
                {
                    "source": doc["source_file"],
                    "chunk_index": doc["chunk_index"],
                    "similarity_score": doc["similarity_score"]
                }
                for doc in retrieved_docs  # Use original docs for citation info
            ]

            result = ChatResponse(
                answer=response,
                citations=citations,
                mode="full_rag",
                session_id=session_id
            )

        # If translation was needed, translate the response back to the target language
        if needs_translation:
            try:
                # Translate the English response to the target language
                result.answer = translation_agent.translate_text(
                    result.answer,
                    target_language,  # Translate to user's language
                    "en"  # From English
                )
            except Exception as e:
                logger.warning(f"Response translation failed, returning English response: {str(e)}")
                # If response translation fails, return the English response

        # Save user message and assistant response to session history
        # Save original query and selected text (in user's language)
        session_manager.save_message(
            session_id=session_id,
            role="user",
            content=request.query,  # Save original query
            selected_text=request.selected_text  # Save original selected text
        )

        # Save response in the language it was returned (could be translated)
        session_manager.save_message(
            session_id=session_id,
            role="assistant",
            content=result.answer,  # Save the potentially translated response
            citations=result.citations
        )

        # Add session_id to response for frontend tracking
        # Note: The response model doesn't include session_id, but we could extend it if needed
        return result

    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")