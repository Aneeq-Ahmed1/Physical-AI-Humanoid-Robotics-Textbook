"""
Tests for the subagent system implementing reusable intelligence via Claude Subagents & Agent Skills.
"""
import pytest
from agent.subagents.book_expert_agent import BookExpertAgent
from agent.subagents.selected_text_agent import SelectedTextAgent
from agent.subagents.chapter_guide_agent import ChapterGuideAgent
from agent.subagents.evaluation_agent import EvaluationAgent
from agent.base_agent import AgentRequest
from agent.skill_registry import list_skills


def test_book_expert_agent_creation():
    """Test that Book Expert Agent can be created properly."""
    agent = BookExpertAgent()
    assert agent.name == "book_expert"
    assert "retrieve_book_chunks" in agent.skills
    assert "answers" in agent.description.lower()


def test_selected_text_agent_creation():
    """Test that Selected Text Agent can be created properly."""
    agent = SelectedTextAgent()
    assert agent.name == "selected_text"
    assert "answer_from_selected_text" in agent.skills
    assert "selected" in agent.description.lower()


def test_chapter_guide_agent_creation():
    """Test that Chapter Guide Agent can be created properly."""
    agent = ChapterGuideAgent()
    assert agent.name == "chapter_guide"
    assert "summarize_chapter" in agent.skills
    assert "explain_like_five" in agent.skills
    assert "difficulty" in agent.description.lower()


def test_evaluation_agent_creation():
    """Test that Evaluation Agent can be created properly."""
    agent = EvaluationAgent()
    assert agent.name == "evaluation"
    assert "hallucination_detection" in agent.skills
    assert "checks" in agent.description.lower()


def test_agent_request_validation():
    """Test that agent request validation works properly."""
    book_agent = BookExpertAgent()

    # Valid request
    valid_request = AgentRequest(query="What is humanoid robotics?")
    assert book_agent.validate_request(valid_request) == True

    # Invalid request (empty query)
    invalid_request = AgentRequest(query="")
    assert book_agent.validate_request(invalid_request) == False


def test_skill_registry():
    """Test that skills are properly registered."""
    skills = list_skills()
    assert len(skills) > 0

    # Check that key skills exist
    expected_skills = [
        "retrieve_book_chunks",
        "answer_from_selected_text",
        "summarize_chapter",
        "explain_like_five",
        "hallucination_detection"
    ]

    for skill_id in expected_skills:
        assert skill_id in skills, f"Skill {skill_id} not found in registry"


def test_book_expert_process_request():
    """Test that Book Expert Agent can process requests."""
    agent = BookExpertAgent()
    request = AgentRequest(query="Test query about humanoid robotics")

    response = agent.process_request(request)

    # Response should have content, confidence, and sources
    assert response.content is not None
    assert isinstance(response.confidence, float)
    assert isinstance(response.sources, list)


def test_selected_text_agent_process_request():
    """Test that Selected Text Agent can process requests."""
    agent = SelectedTextAgent()
    request = AgentRequest(
        query="Explain this concept",
        user_context={"selected_text": "This is the selected text about robotics."}
    )

    response = agent.process_request(request)

    # Response should have content, confidence, and sources
    assert response.content is not None
    assert isinstance(response.confidence, float)
    assert isinstance(response.sources, list)


def test_chapter_guide_agent_process_request():
    """Test that Chapter Guide Agent can process requests."""
    agent = ChapterGuideAgent()
    request = AgentRequest(query="What is inverse kinematics?")

    response = agent.process_request(request)

    # Response should have content, confidence, and sources
    assert response.content is not None
    assert isinstance(response.confidence, float)
    assert isinstance(response.sources, list)


def test_evaluation_agent_process_request():
    """Test that Evaluation Agent can process requests."""
    agent = EvaluationAgent()
    request = AgentRequest(
        query="Evaluate this response",
        user_context={
            "response_to_evaluate": "This is a test response that should be evaluated.",
            "original_query": "What is the meaning of life?"
        }
    )

    response = agent.process_request(request)

    # Response should have content, confidence, and sources
    assert response.content is not None
    assert isinstance(response.confidence, float)
    assert isinstance(response.sources, list)


if __name__ == "__main__":
    # Run tests
    test_book_expert_agent_creation()
    test_selected_text_agent_creation()
    test_chapter_guide_agent_creation()
    test_evaluation_agent_creation()
    test_agent_request_validation()
    test_skill_registry()
    test_book_expert_process_request()
    test_selected_text_agent_process_request()
    test_chapter_guide_agent_process_request()
    test_evaluation_agent_process_request()
    print("All tests passed!")