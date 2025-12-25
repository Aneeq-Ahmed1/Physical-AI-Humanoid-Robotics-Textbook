from ..base_agent import BaseAgent, AgentRequest, AgentResponse
from ..skill_registry import execute_skill
from typing import Dict, Any, Optional
import logging


logger = logging.getLogger(__name__)


class ChapterGuideAgent(BaseAgent):
    """Agent that explains concepts at beginner/intermediate/advanced levels."""

    def __init__(self):
        super().__init__(
            name="chapter_guide",
            description="Explains concepts at different difficulty levels (beginner, intermediate, advanced) and adjusts explanations to match the user's preferred difficulty level",
            skills=["summarize_chapter", "explain_like_five"]
        )

    def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process a request by explaining concepts at the appropriate difficulty level.

        Args:
            request: The request containing the topic and difficulty preference

        Returns:
            AgentResponse with the explanation at the requested difficulty level
        """
        if not self.validate_request(request):
            return AgentResponse(
                content="Invalid request: query is required",
                confidence=0.0,
                sources=[],
                metadata={"error": "invalid_request"}
            )

        try:
            # Determine difficulty level from user context
            user_context = request.user_context or {}
            difficulty = user_context.get('difficulty_preference', 'intermediate').lower()
            chapter = user_context.get('chapter', None)
            chapter_content = user_context.get('chapter_content', request.query)  # Use chapter_content if provided, otherwise use query

            # Generate appropriate explanation based on difficulty
            if difficulty == 'beginner':
                response_content = self._explain_beginner_level(chapter_content, chapter)
            elif difficulty == 'advanced':
                response_content = self._explain_advanced_level(chapter_content, chapter)
            else:  # intermediate (default)
                response_content = self._explain_intermediate_level(chapter_content, chapter)

            return AgentResponse(
                content=response_content,
                confidence=0.85,
                sources=[f"chapter_guide_{difficulty}_level"],
                metadata={
                    "agent": self.name,
                    "difficulty_level": difficulty,
                    "chapter": chapter
                }
            )

        except Exception as e:
            logger.error(f"Error processing request in ChapterGuideAgent: {e}")
            return AgentResponse(
                content="An error occurred while processing your request",
                confidence=0.0,
                sources=[],
                metadata={"error": str(e), "agent": self.name}
            )

    def _explain_beginner_level(self, chapter_content: str, chapter: Optional[str]) -> str:
        """Generate a beginner-level explanation of the chapter content.

        Args:
            chapter_content: The full chapter content to explain at beginner level
            chapter: Optional specific chapter reference

        Returns:
            Beginner-friendly explanation
        """
        # Connect to the LLM to generate a beginner-friendly explanation
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        from agent.llm_agent import LLMAgent

        llm_agent = LLMAgent()

        query = f"Explain the following content in simple terms suitable for a beginner in humanoid robotics. Use analogies and avoid complex technical jargon: {chapter_content[:1000]}"

        # Create a message to send to the LLM that specifically asks for beginner-level explanation
        response = llm_agent.generate_response_selected_text(
            query=query,
            selected_text=chapter_content
        )

        return f"BEGINNER LEVEL EXPLANATION:\n\n{response}\n\nThis simplified explanation focuses on core concepts. Key points for beginners:\n- Main ideas are highlighted\n- Technical jargon is explained in simple terms\n- Practical examples are emphasized\n- Complex mathematical details are summarized"

    def _explain_intermediate_level(self, chapter_content: str, chapter: Optional[str]) -> str:
        """Generate an intermediate-level explanation of the chapter content.

        Args:
            chapter_content: The full chapter content to explain at intermediate level
            chapter: Optional specific chapter reference

        Returns:
            Intermediate-level explanation
        """
        # Connect to the LLM to generate an intermediate-level explanation
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        from agent.llm_agent import LLMAgent

        llm_agent = LLMAgent()

        query = f"Explain the following content at an intermediate level suitable for someone with basic knowledge of humanoid robotics. Include technical details with context, implementation considerations, and practical applications: {chapter_content[:1000]}"

        # Create a message to send to the LLM that specifically asks for intermediate-level explanation
        response = llm_agent.generate_response_selected_text(
            query=query,
            selected_text=chapter_content
        )

        return f"INTERMEDIATE LEVEL EXPLANATION:\n\n{response}\n\nThis explanation includes:\n- Technical details with context\n- Implementation considerations\n- Design trade-offs\n- Practical applications"

    def _explain_advanced_level(self, chapter_content: str, chapter: Optional[str]) -> str:
        """Generate an advanced-level explanation of the chapter content.

        Args:
            chapter_content: The full chapter content to explain at advanced level
            chapter: Optional specific chapter reference

        Returns:
            Advanced-level explanation
        """
        # Connect to the LLM to generate an advanced-level explanation
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        from agent.llm_agent import LLMAgent

        llm_agent = LLMAgent()

        query = f"Explain the following content at an advanced level suitable for experts in humanoid robotics. Include mathematical foundations, research implications, cutting-edge developments, implementation challenges, and performance considerations: {chapter_content[:1000]}"

        # Create a message to send to the LLM that specifically asks for advanced-level explanation
        response = llm_agent.generate_response_selected_text(
            query=query,
            selected_text=chapter_content
        )

        return f"ADVANCED LEVEL EXPLANATION:\n\n{response}\n\nThis advanced explanation includes:\n- Mathematical foundations\n- Research implications\n- Cutting-edge developments\n- Implementation challenges\n- Performance considerations"

    def validate_request(self, request: AgentRequest) -> bool:
        """Validate the request, ensuring a topic is provided.

        Args:
            request: The request to validate

        Returns:
            True if request is valid, False otherwise
        """
        return bool(request.query and request.query.strip())

    def _simplify_for_beginner(self, text: str) -> str:
        """Simplify text for beginner level understanding."""
        # Replace complex technical terms with simpler explanations
        simplified = text.replace("algorithm", "step-by-step process")
        simplified = simplified.replace("optimization", "making something work better")
        simplified = simplified.replace("implementation", "how it's built")
        simplified = simplified.replace("parameter", "setting")
        simplified = simplified.replace("framework", "toolkit")
        simplified = simplified.replace("abstraction", "simplified model")
        simplified = simplified.replace("decomposition", "breaking into parts")
        return simplified

    def _add_context_for_intermediate(self, text: str) -> str:
        """Add context and implementation details for intermediate level."""
        # Keep technical terms but add context
        return text

    def _add_analysis_for_advanced(self, text: str) -> str:
        """Add advanced technical analysis for expert level."""
        # Keep all technical details and add deeper analysis
        return text