from ..base_agent import BaseAgent, AgentRequest, AgentResponse
from ..skill_registry import execute_skill
from typing import Dict, Any, Optional
import logging


logger = logging.getLogger(__name__)


class BookExpertAgent(BaseAgent):
    """Agent that answers questions using full-book RAG capabilities."""

    def __init__(self):
        super().__init__(
            name="book_expert",
            description="Answers questions using full-book RAG capabilities, leveraging the entire textbook content through retrieval-augmented generation techniques",
            skills=["retrieve_book_chunks"]
        )

    def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process a request using book expertise and RAG capabilities.

        Args:
            request: The request containing the query and context

        Returns:
            AgentResponse with the answer based on book content
        """
        if not self.validate_request(request):
            return AgentResponse(
                content="Invalid request: query is required",
                confidence=0.0,
                sources=[],
                metadata={"error": "invalid_request"}
            )

        try:
            # Use the retrieve_book_chunks skill to get relevant content
            chunks = execute_skill(
                "retrieve_book_chunks",
                query=request.query,
                max_chunks=5
            )

            if not chunks:
                return AgentResponse(
                    content="No relevant content found in the book for your query",
                    confidence=0.3,
                    sources=[],
                    metadata={"status": "no_content_found"}
                )

            # Prepare context for the LLM from the retrieved chunks
            context = self._format_chunks_for_llm(chunks)

            # Connect to the LLM to generate a proper response based on the RAG results
            from backend.agent.llm_agent import LLMAgent

            llm_agent = LLMAgent()
            response_content = llm_agent.generate_response_full_rag(
                query=request.query,
                context_documents=chunks
            )

            # Extract source information
            sources = [chunk.get('source', 'unknown') for chunk in chunks if 'source' in chunk]

            return AgentResponse(
                content=response_content,
                confidence=0.8,  # High confidence for RAG-based responses
                sources=sources,
                metadata={
                    "chunks_used": len(chunks),
                    "agent": self.name
                }
            )

        except Exception as e:
            logger.error(f"Error processing request in BookExpertAgent: {e}")
            return AgentResponse(
                content="An error occurred while processing your request",
                confidence=0.0,
                sources=[],
                metadata={"error": str(e), "agent": self.name}
            )

