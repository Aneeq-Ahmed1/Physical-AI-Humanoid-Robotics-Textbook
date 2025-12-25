from typing import Dict, List, Optional, Any
from .base_agent import BaseAgent, AgentRequest, AgentResponse
import re


class AgentRouter:
    """Routes requests to the appropriate agent based on content analysis."""

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.routing_rules: Dict[str, List[str]] = {}

    def register_agent(self, agent: BaseAgent):
        """Register an agent with the router.

        Args:
            agent: The agent to register
        """
        self.agents[agent.name] = agent
        # Default routing rules based on agent name and description
        self.routing_rules[agent.name] = self._generate_routing_keywords(agent)

    def _generate_routing_keywords(self, agent: BaseAgent) -> List[str]:
        """Generate routing keywords based on agent name and description.

        Args:
            agent: The agent to generate keywords for

        Returns:
            List of keywords associated with this agent
        """
        keywords = []
        name_lower = agent.name.lower()
        desc_lower = agent.description.lower()

        if 'book' in name_lower or 'expert' in name_lower or 'comprehensive' in desc_lower:
            keywords.extend(['book', 'expert', 'comprehensive', 'detailed', 'full', 'complete', 'reference'])

        if 'text' in name_lower or 'selected' in name_lower or 'analyze' in desc_lower:
            keywords.extend(['analyze', 'selected', 'text', 'focus', 'specific', 'highlighted'])

        if 'chapter' in name_lower or 'guide' in name_lower or 'explain' in desc_lower:
            keywords.extend(['explain', 'guide', 'chapter', 'concept', 'understand', 'learning', 'teaching'])

        if 'evaluate' in name_lower or 'quality' in desc_lower or 'check' in desc_lower:
            keywords.extend(['evaluate', 'quality', 'check', 'verify', 'accuracy', 'hallucination', 'validation'])

        return keywords

    def route_request(self, request: AgentRequest) -> AgentResponse:
        """Route a request to the most appropriate agent.

        Args:
            request: The request to route

        Returns:
            AgentResponse from the selected agent
        """
        # Determine the best agent for this request
        selected_agent = self._select_agent(request)

        if selected_agent is None:
            # If no agent is found, return an error response
            return AgentResponse(
                content="No suitable agent found for this request",
                confidence=0.0,
                sources=[],
                metadata={"error": "no_agent_found"}
            )

        # Process the request with the selected agent
        return selected_agent.process_request(request)

    def _select_agent(self, request: AgentRequest) -> Optional[BaseAgent]:
        """Select the most appropriate agent for the given request.

        Args:
            request: The request to analyze

        Returns:
            The most appropriate agent, or None if no match is found
        """
        query_lower = request.query.lower()
        user_context = request.user_context or {}

        # Check if a specific agent is requested in user context
        if 'preferred_agent' in user_context:
            preferred_agent = user_context['preferred_agent']
            if preferred_agent in self.agents:
                return self.agents[preferred_agent]

        # Score each agent based on keyword matching
        agent_scores = {}
        for agent_name, agent in self.agents.items():
            score = self._calculate_agent_score(agent_name, agent, query_lower)
            agent_scores[agent_name] = score

        # Find the agent with the highest score
        if agent_scores:
            best_agent_name = max(agent_scores, key=agent_scores.get)
            if agent_scores[best_agent_name] > 0:
                return self.agents[best_agent_name]

        # If no keyword matches, use a default agent if available
        # For now, return the first available agent as a fallback
        if self.agents:
            return list(self.agents.values())[0]

        return None

    def _calculate_agent_score(self, agent_name: str, agent: BaseAgent, query_lower: str) -> float:
        """Calculate a score for how well an agent matches the query.

        Args:
            agent_name: Name of the agent
            agent: The agent object
            query_lower: Lowercase version of the query

        Returns:
            A score between 0 and 1 indicating match quality
        """
        score = 0
        keywords = self.routing_rules.get(agent_name, [])

        # Count keyword matches
        for keyword in keywords:
            if keyword in query_lower:
                score += 1

        # Additional heuristics
        if 'book' in agent_name.lower() or 'expert' in agent_name.lower():
            # Book expert gets bonus for complex questions
            if any(word in query_lower for word in ['relationship', 'connection', 'overview', 'summary', 'comprehensive']):
                score += 0.5

        if 'selected' in agent_name.lower() or 'text' in agent_name.lower():
            # Selected text agent gets bonus for analysis requests
            if any(word in query_lower for word in ['analyze', 'specific', 'focus', 'only', 'just', 'text']):
                score += 0.5

        if 'chapter' in agent_name.lower() or 'guide' in agent_name.lower():
            # Chapter guide gets bonus for explanation requests
            if any(word in query_lower for word in ['explain', 'how', 'what is', 'understand', 'learning']):
                score += 0.5

        if 'evaluate' in agent_name.lower():
            # Evaluation agent gets bonus for quality check requests
            if any(word in query_lower for word in ['evaluate', 'check', 'quality', 'verify', 'accurate', 'correct']):
                score += 0.5

        return score

    def get_available_agents(self) -> List[str]:
        """Get list of available agent names.

        Returns:
            List of agent names
        """
        return list(self.agents.keys())

    def initialize_agents(self):
        """Initialize all agents and register them with the router."""
        # This method will be called after all agents are defined to register them
        # Actual agent registration will happen in other modules
        pass


# Global router instance
router = AgentRouter()


def get_router() -> AgentRouter:
    """Get the global agent router instance.

    Returns:
        The global AgentRouter instance
    """
    return router