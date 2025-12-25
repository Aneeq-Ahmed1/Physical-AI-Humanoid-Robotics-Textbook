from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import logging
import sys
import os

# Add the backend directory to Python path to handle relative imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.agent_router import get_router
from agent.base_agent import AgentRequest, AgentResponse
from agent.subagents.book_expert_agent import BookExpertAgent
from agent.subagents.selected_text_agent import SelectedTextAgent
from agent.subagents.chapter_guide_agent import ChapterGuideAgent
from agent.subagents.evaluation_agent import EvaluationAgent
from agent.evaluation import evaluate_response


logger = logging.getLogger(__name__)
router = APIRouter()


# Initialize and register agents
def register_agents_with_router():
    """Register all subagents with the agent router."""
    agent_router = get_router()

    # Register Book Expert Agent
    if "book_expert" not in agent_router.get_available_agents():
        book_agent = BookExpertAgent()
        agent_router.register_agent(book_agent)
        logger.info(f"Registered agent: {book_agent.name}")

    # Register Selected Text Agent
    if "selected_text" not in agent_router.get_available_agents():
        selected_agent = SelectedTextAgent()
        agent_router.register_agent(selected_agent)
        logger.info(f"Registered agent: {selected_agent.name}")

    # Register Chapter Guide Agent
    if "chapter_guide" not in agent_router.get_available_agents():
        chapter_agent = ChapterGuideAgent()
        agent_router.register_agent(chapter_agent)
        logger.info(f"Registered agent: {chapter_agent.name}")

    # Register Evaluation Agent
    if "evaluation" not in agent_router.get_available_agents():
        eval_agent = EvaluationAgent()
        agent_router.register_agent(eval_agent)
        logger.info(f"Registered agent: {eval_agent.name}")

    logger.info(f"Total registered agents: {len(agent_router.get_available_agents())}")


# Register agents when module is imported
register_agents_with_router()


class AgentRequestModel(BaseModel):
    query: str
    user_context: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class AgentResponseModel(BaseModel):
    request_id: str
    agent_used: str
    response: str
    confidence: float
    sources: List[str]
    evaluation: Optional[Dict[str, Any]] = None
    timestamp: str


class BookExpertRequest(BaseModel):
    query: str
    context: str = "full_book"
    include_sources: bool = True


class SelectedTextRequest(BaseModel):
    selected_text: str
    analysis_type: str = "analysis"
    context_isolation: bool = True


class ChapterGuideRequest(BaseModel):
    topic: str
    chapter: Optional[str] = None
    difficulty: str = "intermediate"
    include_examples: bool = True


class EvaluationRequest(BaseModel):
    response_to_evaluate: str
    original_query: str
    expected_context: Optional[str] = None


@router.post("/subagent", response_model=AgentResponseModel)
async def route_agent_request(request: AgentRequestModel):
    """Route request to the most appropriate agent based on content analysis."""
    try:
        from datetime import datetime
        import uuid

        # Create agent request object
        agent_request = AgentRequest(
            query=request.query,
            user_context=request.user_context,
            metadata=request.metadata
        )

        # Get the router and route the request
        agent_router = get_router()

        response = agent_router.route_request(agent_request)

        # Evaluate the response quality
        evaluation_result = evaluate_response(
            response=response.content,
            original_query=request.query,
            expected_context=request.metadata.get('context', '') if request.metadata else ''
        ) if response.content else None

        # Generate response model
        response_model = AgentResponseModel(
            request_id=str(uuid.uuid4()),
            agent_used=response.metadata.get('agent', 'unknown') if response.metadata else 'unknown',
            response=response.content,
            confidence=response.confidence,
            sources=response.sources,
            evaluation={
                "quality_score": evaluation_result.quality_score,
                "issues": evaluation_result.issues,
                "suggestions": evaluation_result.suggestions,
                "confidence_in_evaluation": evaluation_result.confidence_in_evaluation
            } if evaluation_result else None,
            timestamp=datetime.now().isoformat()
        )

        return response_model

    except Exception as e:
        logger.error(f"Error routing agent request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/subagent/book-expert", response_model=AgentResponseModel)
async def book_expert_endpoint(request: BookExpertRequest):
    """Direct access to the Book Expert Agent."""
    try:
        from datetime import datetime
        import uuid

        # Create agent request
        agent_request = AgentRequest(
            query=request.query,
            user_context={"context_type": request.context},
            metadata={"include_sources": request.include_sources}
        )

        # Use the registered Book Expert Agent from the router
        agent_router = get_router()
        book_agent = None

        # Find the book expert agent in registered agents
        for agent_name in agent_router.get_available_agents():
            if agent_name == "book_expert":
                # Get the registered agent instance from the router
                book_agent = agent_router.agents[agent_name]
                break

        if book_agent:
            response = book_agent.process_request(agent_request)
        else:
            # Fallback: create and use agent directly
            book_agent = BookExpertAgent()
            response = book_agent.process_request(agent_request)

        # Evaluate the response
        evaluation_result = evaluate_response(
            response=response.content,
            original_query=request.query
        )

        response_model = AgentResponseModel(
            request_id=str(uuid.uuid4()),
            agent_used="book_expert",
            response=response.content,
            confidence=response.confidence,
            sources=response.sources,
            evaluation={
                "quality_score": evaluation_result.quality_score,
                "issues": evaluation_result.issues,
                "suggestions": evaluation_result.suggestions,
                "confidence_in_evaluation": evaluation_result.confidence_in_evaluation
            },
            timestamp=datetime.now().isoformat()
        )

        return response_model

    except Exception as e:
        logger.error(f"Error in book expert endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/subagent/selected-text", response_model=AgentResponseModel)
async def selected_text_endpoint(request: SelectedTextRequest):
    """Direct access to the Selected Text Agent."""
    try:
        from datetime import datetime
        import uuid

        # Create agent request with selected text in user context
        agent_request = AgentRequest(
            query=request.selected_text if request.analysis_type == "analysis" else request.selected_text + " " + request.analysis_type,
            user_context={
                "selected_text": request.selected_text,
                "analysis_type": request.analysis_type,
                "context_isolation": request.context_isolation
            },
            metadata={}
        )

        # Use the registered Selected Text Agent from the router
        agent_router = get_router()
        selected_agent = None

        # Find the selected text agent in registered agents
        for agent_name in agent_router.get_available_agents():
            if agent_name == "selected_text":
                # Get the registered agent instance from the router
                selected_agent = agent_router.agents[agent_name]
                break

        if selected_agent:
            response = selected_agent.process_request(agent_request)
        else:
            # Fallback: create and use agent directly
            selected_agent = SelectedTextAgent()
            response = selected_agent.process_request(agent_request)

        # Evaluate the response
        evaluation_result = evaluate_response(
            response=response.content,
            original_query=request.selected_text
        )

        response_model = AgentResponseModel(
            request_id=str(uuid.uuid4()),
            agent_used="selected_text",
            response=response.content,
            confidence=response.confidence,
            sources=response.sources,
            evaluation={
                "quality_score": evaluation_result.quality_score,
                "issues": evaluation_result.issues,
                "suggestions": evaluation_result.suggestions,
                "confidence_in_evaluation": evaluation_result.confidence_in_evaluation
            },
            timestamp=datetime.now().isoformat()
        )

        return response_model

    except Exception as e:
        logger.error(f"Error in selected text endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/subagent/chapter-guide", response_model=AgentResponseModel)
async def chapter_guide_endpoint(request: ChapterGuideRequest):
    """Direct access to the Chapter Guide Agent."""
    try:
        from datetime import datetime
        import uuid

        # Create agent request with difficulty preference in user context
        agent_request = AgentRequest(
            query=request.topic,
            user_context={
                "difficulty_preference": request.difficulty,
                "chapter": request.chapter
            },
            metadata={"include_examples": request.include_examples}
        )

        # Use the registered Chapter Guide Agent from the router
        agent_router = get_router()
        chapter_agent = None

        # Find the chapter guide agent in registered agents
        for agent_name in agent_router.get_available_agents():
            if agent_name == "chapter_guide":
                # Get the registered agent instance from the router
                chapter_agent = agent_router.agents[agent_name]
                break

        if chapter_agent:
            response = chapter_agent.process_request(agent_request)
        else:
            # Fallback: create and use agent directly
            chapter_agent = ChapterGuideAgent()
            response = chapter_agent.process_request(agent_request)

        # Evaluate the response
        evaluation_result = evaluate_response(
            response=response.content,
            original_query=request.topic
        )

        response_model = AgentResponseModel(
            request_id=str(uuid.uuid4()),
            agent_used="chapter_guide",
            response=response.content,
            confidence=response.confidence,
            sources=response.sources,
            evaluation={
                "quality_score": evaluation_result.quality_score,
                "issues": evaluation_result.issues,
                "suggestions": evaluation_result.suggestions,
                "confidence_in_evaluation": evaluation_result.confidence_in_evaluation
            },
            timestamp=datetime.now().isoformat()
        )

        return response_model

    except Exception as e:
        logger.error(f"Error in chapter guide endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/subagent/evaluate", response_model=AgentResponseModel)
async def evaluation_endpoint(request: EvaluationRequest):
    """Direct access to the Evaluation Agent."""
    try:
        from datetime import datetime
        import uuid

        # Create agent request with evaluation context
        agent_request = AgentRequest(
            query=f"Evaluate this response: {request.response_to_evaluate}",
            user_context={
                "response_to_evaluate": request.response_to_evaluate,
                "original_query": request.original_query,
                "expected_context": request.expected_context
            },
            metadata={}
        )

        # Use the registered Evaluation Agent from the router
        agent_router = get_router()
        eval_agent = None

        # Find the evaluation agent in registered agents
        for agent_name in agent_router.get_available_agents():
            if agent_name == "evaluation":
                # Get the registered agent instance from the router
                eval_agent = agent_router.agents[agent_name]
                break

        if eval_agent:
            response = eval_agent.process_request(agent_request)
        else:
            # Fallback: create and use agent directly
            eval_agent = EvaluationAgent()
            response = eval_agent.process_request(agent_request)

        # For the evaluation agent, we don't need to re-evaluate the evaluation
        response_model = AgentResponseModel(
            request_id=str(uuid.uuid4()),
            agent_used="evaluation",
            response=response.content,
            confidence=response.confidence,
            sources=response.sources,
            evaluation={
                "quality_score": response.metadata.get("quality_score", 0.5) if response.metadata else 0.5,
                "issues": response.metadata.get("issues", []) if response.metadata else [],
                "suggestions": response.metadata.get("suggestions", []) if response.metadata else [],
                "confidence_in_evaluation": response.confidence
            },
            timestamp=datetime.now().isoformat()
        )

        return response_model

    except Exception as e:
        logger.error(f"Error in evaluation endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))