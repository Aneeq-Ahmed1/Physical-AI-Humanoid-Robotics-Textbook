from ..base_agent import BaseAgent, AgentRequest, AgentResponse
from ..skill_registry import execute_skill
from typing import Dict, Any, Optional
import logging


logger = logging.getLogger(__name__)


class SelectedTextAgent(BaseAgent):
    """Agent that answers questions based only on selected text without pulling in external information."""

    def __init__(self):
        super().__init__(
            name="selected_text",
            description="Answers questions based on selected/highlighted text only, without pulling in external information or book content",
            skills=["answer_from_selected_text"]
        )

    def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process a request using only the selected text.

        Args:
            request: The request containing the selected text and question

        Returns:
            AgentResponse with the answer based only on the selected text
        """
        if not self.validate_request(request):
            return AgentResponse(
                content="Invalid request: query is required",
                confidence=0.0,
                sources=[],
                metadata={"error": "invalid_request"}
            )

        # Extract selected text from user context or metadata
        user_context = request.user_context or {}
        selected_text = user_context.get('selected_text', '')

        if not selected_text:
            return AgentResponse(
                content="No selected text provided. This agent requires specific text to analyze.",
                confidence=0.0,
                sources=[],
                metadata={"error": "no_selected_text"}
            )

        try:
            # Use the answer_from_selected_text skill to process the request
            response_content = execute_skill(
                "answer_from_selected_text",
                selected_text=selected_text,
                question=request.query
            )

            # Verify that the response is based only on the provided text
            # (In a real implementation, this would be enforced by the skill)
            sources = [f"selected_text_{len(selected_text)}_chars"]

            return AgentResponse(
                content=response_content,
                confidence=0.9,  # High confidence when working with specific text
                sources=sources,
                metadata={
                    "agent": self.name,
                    "text_length": len(selected_text)
                }
            )

        except Exception as e:
            logger.error(f"Error processing request in SelectedTextAgent: {e}")
            return AgentResponse(
                content="An error occurred while processing your request",
                confidence=0.0,
                sources=[],
                metadata={"error": str(e), "agent": self.name}
            )

    def validate_request(self, request: AgentRequest) -> bool:
        """Validate the request, ensuring selected text is provided.

        Args:
            request: The request to validate

        Returns:
            True if request is valid, False otherwise
        """
        if not request.query or not request.query.strip():
            return False

        # Check if selected text is provided in user context
        user_context = request.user_context or {}
        selected_text = user_context.get('selected_text', '')

        return bool(selected_text and selected_text.strip())