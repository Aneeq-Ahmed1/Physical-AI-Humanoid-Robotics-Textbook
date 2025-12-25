from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class AgentRequest:
    """Represents a request to an agent."""
    query: str
    user_context: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    agent_context: Optional[Dict[str, Any]] = None


@dataclass
class AgentResponse:
    """Represents a response from an agent."""
    content: str
    confidence: float = 1.0
    sources: List[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.sources is None:
            self.sources = []


class BaseAgent(ABC):
    """Abstract base class for all agents in the system."""

    def __init__(self, name: str, description: str, skills: List[str] = None):
        self.name = name
        self.description = description
        self.skills = skills or []

    @abstractmethod
    def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process an agent request and return a response.

        Args:
            request: The request to process

        Returns:
            AgentResponse containing the result
        """
        pass

    def get_available_skills(self) -> List[str]:
        """Get list of skills available to this agent.

        Returns:
            List of skill names
        """
        return self.skills.copy()

    def validate_request(self, request: AgentRequest) -> bool:
        """Validate the incoming request.

        Args:
            request: The request to validate

        Returns:
            True if request is valid, False otherwise
        """
        return bool(request.query and request.query.strip())

    def execute_skill(self, skill_id: str, **kwargs) -> Any:
        """Execute a skill with the given parameters.

        Args:
            skill_id: ID of the skill to execute
            **kwargs: Parameters for the skill

        Returns:
            Result of the skill execution
        """
        from .skill_registry import get_skill
        skill_func = get_skill(skill_id)
        if skill_func is None:
            raise ValueError(f"Skill '{skill_id}' not found")
        return skill_func(**kwargs)