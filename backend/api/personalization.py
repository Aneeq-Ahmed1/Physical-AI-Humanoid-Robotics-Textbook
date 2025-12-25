"""API endpoints for content personalization."""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
import sys
import os
import uuid
from datetime import datetime

# Add the backend directory to Python path to handle relative imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.agent_router import get_router
from agent.base_agent import AgentRequest, AgentResponse
from agent.subagents.chapter_guide_agent import ChapterGuideAgent
from .personalization_cache import personalization_cache, PersonalizationSession

logger = logging.getLogger(__name__)
router = APIRouter()


class PersonalizeContentRequest(BaseModel):
    """Request model for content personalization."""
    session_id: str
    chapter_content: str
    difficulty_level: str  # 'beginner', 'intermediate', 'advanced'
    chapter_id: str
    reading_position: Optional[int] = 0


class PersonalizeContentResponse(BaseModel):
    """Response model for content personalization."""
    session_id: str
    personalized_content: str
    difficulty_level: str
    chapter_id: str
    timestamp: str


class ToggleOriginalContentRequest(BaseModel):
    """Request model for toggling back to original content."""
    session_id: str


class ToggleOriginalContentResponse(BaseModel):
    """Response model for toggling back to original content."""
    session_id: str
    original_content: str
    timestamp: str


@router.post("/personalize", response_model=PersonalizeContentResponse)
async def personalize_content(request: PersonalizeContentRequest):
    """Personalize chapter content based on difficulty level."""
    try:
        # Validate required fields
        if not request.session_id or not request.session_id.strip():
            raise HTTPException(
                status_code=400,
                detail="Session ID is required and cannot be empty"
            )

        if not request.chapter_content or not request.chapter_content.strip():
            raise HTTPException(
                status_code=400,
                detail="Chapter content is required and cannot be empty"
            )

        if not request.chapter_id or not request.chapter_id.strip():
            raise HTTPException(
                status_code=400,
                detail="Chapter ID is required and cannot be empty"
            )

        # Validate difficulty level
        valid_levels = ['beginner', 'intermediate', 'advanced']
        difficulty_level = request.difficulty_level.lower()
        if difficulty_level not in valid_levels:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid difficulty level '{request.difficulty_level}'. Must be one of: {valid_levels}"
            )

        # Periodically clean up expired sessions (approximately 1 in 10 requests)
        import random
        if random.randint(1, 10) == 1:  # 10% chance to cleanup
            expired_count = personalization_cache.cleanup_expired_sessions()
            if expired_count > 0:
                logger.info(f"Cleaned up {expired_count} expired sessions")

        # Get or create personalization session
        session = personalization_cache.get_session(request.session_id)
        if session:
            logger.info(f"Updating existing session {request.session_id} with difficulty level {difficulty_level}")
            # Update existing session
            personalization_cache.update_difficulty_level(request.session_id, difficulty_level)
            personalization_cache.update_reading_position(request.session_id, request.reading_position)
        else:
            logger.info(f"Creating new session {request.session_id} with difficulty level {difficulty_level}")
            # Create new session
            session = personalization_cache.create_session(
                session_id=request.session_id,
                difficulty_level=difficulty_level,
                original_content=request.chapter_content,
                chapter_id=request.chapter_id,
                reading_position=request.reading_position
            )

        # Process content with Chapter Guide Agent
        agent_router = get_router()
        chapter_agent = None

        # Find the chapter guide agent in registered agents
        for agent_name in agent_router.get_available_agents():
            if agent_name == "chapter_guide":
                chapter_agent = agent_router.agents[agent_name]
                break

        if not chapter_agent:
            logger.warning("Chapter guide agent not found in router, using fallback")
            # Fallback: create and use agent directly
            chapter_agent = ChapterGuideAgent()

        # Create agent request with chapter content and difficulty preference
        agent_request = AgentRequest(
            query=request.chapter_content,
            user_context={
                "difficulty_preference": difficulty_level,
                "chapter": request.chapter_id,
                "chapter_content": request.chapter_content
            },
            metadata={}
        )

        # Process the request
        logger.info(f"Processing personalization request for session {request.session_id}, difficulty: {difficulty_level}")
        response = chapter_agent.process_request(agent_request)

        if not response.content or ("error" in response.metadata if response.metadata else {}):
            error_detail = response.metadata.get("error", "Unknown error") if response.metadata else "Unknown error"
            logger.error(f"Chapter Guide Agent failed to process content: {error_detail}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to process content with Chapter Guide Agent: {error_detail}"
            )

        # Cache the personalized content
        success = personalization_cache.update_session_content(
            request.session_id,
            response.content
        )

        if not success:
            logger.warning(f"Failed to cache personalized content for session {request.session_id}")
        else:
            logger.info(f"Successfully cached personalized content for session {request.session_id}")

        # Return personalized content
        return PersonalizeContentResponse(
            session_id=request.session_id,
            personalized_content=response.content,
            difficulty_level=difficulty_level,
            chapter_id=request.chapter_id,
            timestamp=datetime.now().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in personalize_content: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/toggle-original", response_model=ToggleOriginalContentResponse)
async def toggle_original_content(request: ToggleOriginalContentRequest):
    """Toggle back to original chapter content."""
    try:
        # Validate session ID
        if not request.session_id or not request.session_id.strip():
            raise HTTPException(
                status_code=400,
                detail="Session ID is required and cannot be empty"
            )

        # Periodically clean up expired sessions (approximately 1 in 10 requests)
        import random
        if random.randint(1, 10) == 1:  # 10% chance to cleanup
            expired_count = personalization_cache.cleanup_expired_sessions()
            if expired_count > 0:
                logger.info(f"Cleaned up {expired_count} expired sessions")

        logger.info(f"Retrieving session {request.session_id} for toggle to original content")
        session = personalization_cache.get_session(request.session_id)
        if not session:
            logger.warning(f"Session {request.session_id} not found for toggle operation")
            raise HTTPException(
                status_code=404,
                detail=f"Personalization session '{request.session_id}' not found"
            )

        logger.info(f"Successfully retrieved original content for session {request.session_id}")
        return ToggleOriginalContentResponse(
            session_id=request.session_id,
            original_content=session.original_content,
            timestamp=datetime.now().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in toggle_original_content: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/change-difficulty")
async def change_difficulty_level(request: PersonalizeContentRequest):
    """Change the difficulty level mid-session and return new personalized content."""
    try:
        # Validate required fields
        if not request.session_id or not request.session_id.strip():
            raise HTTPException(
                status_code=400,
                detail="Session ID is required and cannot be empty"
            )

        if not request.chapter_content or not request.chapter_content.strip():
            raise HTTPException(
                status_code=400,
                detail="Chapter content is required and cannot be empty"
            )

        if not request.chapter_id or not request.chapter_id.strip():
            raise HTTPException(
                status_code=400,
                detail="Chapter ID is required and cannot be empty"
            )

        # Validate difficulty level
        valid_levels = ['beginner', 'intermediate', 'advanced']
        difficulty_level = request.difficulty_level.lower()
        if difficulty_level not in valid_levels:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid difficulty level '{request.difficulty_level}'. Must be one of: {valid_levels}"
            )

        # Periodically clean up expired sessions (approximately 1 in 10 requests)
        import random
        if random.randint(1, 10) == 1:  # 10% chance to cleanup
            expired_count = personalization_cache.cleanup_expired_sessions()
            if expired_count > 0:
                logger.info(f"Cleaned up {expired_count} expired sessions")

        logger.info(f"Changing difficulty level for session {request.session_id} to {difficulty_level}")

        # Update session with new difficulty level
        success = personalization_cache.update_difficulty_level(request.session_id, difficulty_level)
        if not success:
            logger.warning(f"Session {request.session_id} not found for difficulty change")
            raise HTTPException(
                status_code=404,
                detail=f"Personalization session '{request.session_id}' not found"
            )

        # Update reading position
        personalization_cache.update_reading_position(request.session_id, request.reading_position)

        # Get updated session
        session = personalization_cache.get_session(request.session_id)
        if not session:
            logger.error(f"Failed to retrieve updated session {request.session_id} after difficulty change")
            raise HTTPException(
                status_code=500,
                detail="Failed to retrieve updated session after difficulty change"
            )

        # Process content with new difficulty level using Chapter Guide Agent
        agent_router = get_router()
        chapter_agent = None

        # Find the chapter guide agent in registered agents
        for agent_name in agent_router.get_available_agents():
            if agent_name == "chapter_guide":
                chapter_agent = agent_router.agents[agent_name]
                break

        if not chapter_agent:
            logger.warning("Chapter guide agent not found in router, using fallback")
            # Fallback: create and use agent directly
            chapter_agent = ChapterGuideAgent()

        # Create agent request with chapter content and new difficulty preference
        agent_request = AgentRequest(
            query=session.original_content,
            user_context={
                "difficulty_preference": difficulty_level,
                "chapter": request.chapter_id,
                "chapter_content": session.original_content
            },
            metadata={}
        )

        # Process the request
        logger.info(f"Processing difficulty change request for session {request.session_id}, new difficulty: {difficulty_level}")
        response = chapter_agent.process_request(agent_request)

        if not response.content or ("error" in response.metadata if response.metadata else {}):
            error_detail = response.metadata.get("error", "Unknown error") if response.metadata else "Unknown error"
            logger.error(f"Chapter Guide Agent failed to process difficulty change: {error_detail}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to process content with Chapter Guide Agent: {error_detail}"
            )

        # Cache the new personalized content
        success = personalization_cache.update_session_content(
            request.session_id,
            response.content
        )

        if not success:
            logger.warning(f"Failed to cache updated personalized content for session {request.session_id}")
        else:
            logger.info(f"Successfully cached updated personalized content for session {request.session_id}")

        # Return new personalized content
        return PersonalizeContentResponse(
            session_id=request.session_id,
            personalized_content=response.content,
            difficulty_level=difficulty_level,
            chapter_id=request.chapter_id,
            timestamp=datetime.now().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in change_difficulty_level: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/session/{session_id}")
async def clear_personalization_session(session_id: str):
    """Clear a personalization session from cache."""
    try:
        # Validate session ID
        if not session_id or not session_id.strip():
            raise HTTPException(
                status_code=400,
                detail="Session ID is required and cannot be empty"
            )

        logger.info(f"Attempting to clear session {session_id}")
        success = personalization_cache.clear_session(session_id)
        if not success:
            logger.warning(f"Session {session_id} not found for deletion")
            raise HTTPException(
                status_code=404,
                detail=f"Personalization session '{session_id}' not found"
            )

        logger.info(f"Successfully cleared session {session_id}")
        return {"message": "Session cleared successfully", "session_id": session_id}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in clear_personalization_session: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")