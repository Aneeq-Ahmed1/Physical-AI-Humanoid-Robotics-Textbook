"""
Agent system initialization and dependency injection for the subagent architecture.

This module handles the initialization of the agent system and provides
dependency injection for agent components.
"""

from .base_agent import BaseAgent, AgentRequest, AgentResponse
from .agent_router import AgentRouter, get_router
from .skill_registry import (
    register_skill,
    get_skill,
    get_skill_info,
    list_skills,
    execute_skill
)
from .evaluation import (
    EvaluationFramework,
    EvaluationResult,
    evaluate_response
)

# Import all skill modules to ensure skills are registered
from .skills import retrieval_skills
from .skills import text_analysis_skills
from .skills import chapter_skills
from .skills import evaluation_skills

# Import all agent modules to ensure proper initialization
from .subagents import book_expert_agent
from .subagents import selected_text_agent
from .subagents import chapter_guide_agent
from .subagents import evaluation_agent

# Global instances for dependency injection
_agent_router = None
_evaluation_framework = None
_skill_registry = None


def initialize_agent_system():
    """Initialize the agent system and all its components."""
    global _agent_router, _evaluation_framework, _skill_registry

    # Initialize the agent router
    _agent_router = AgentRouter()

    # Initialize the evaluation framework
    _evaluation_framework = EvaluationFramework()

    # The skill registry is automatically initialized when imported
    # Skills will be registered as modules are loaded

    return {
        'router': _agent_router,
        'evaluation': _evaluation_framework,
        'skills': list_skills()
    }


def get_agent_router() -> AgentRouter:
    """Get the agent router instance (dependency injection).

    Returns:
        AgentRouter instance
    """
    global _agent_router
    if _agent_router is None:
        _agent_router = AgentRouter()
    return _agent_router


def get_evaluation_framework() -> EvaluationFramework:
    """Get the evaluation framework instance (dependency injection).

    Returns:
        EvaluationFramework instance
    """
    global _evaluation_framework
    if _evaluation_framework is None:
        _evaluation_framework = EvaluationFramework()
    return _evaluation_framework


def reset_agent_system():
    """Reset the agent system (useful for testing)."""
    global _agent_router, _evaluation_framework, _skill_registry
    _agent_router = None
    _evaluation_framework = None
    _skill_registry = None


# Initialize the system when the module is imported
# This ensures all components are ready when the agent system is used
initialize_agent_system()