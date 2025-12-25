from ..base_agent import BaseAgent, AgentRequest, AgentResponse
from ..skill_registry import execute_skill
from ..evaluation import evaluate_response
from typing import Dict, Any, Optional
import logging


logger = logging.getLogger(__name__)


class EvaluationAgent(BaseAgent):
    """Agent that checks responses for hallucinations and context leakage."""

    def __init__(self):
        super().__init__(
            name="evaluation",
            description="Checks responses for hallucinations, context leakage, and factual accuracy",
            skills=["hallucination_detection"]
        )

    def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process a request by evaluating the provided response.

        Args:
            request: The request containing the response to evaluate

        Returns:
            AgentResponse with the evaluation results
        """
        if not self.validate_request(request):
            return AgentResponse(
                content="Invalid request: response to evaluate is required",
                confidence=0.0,
                sources=[],
                metadata={"error": "invalid_request"}
            )

        try:
            # Extract the response to evaluate from user context or query
            user_context = request.user_context or {}
            response_to_evaluate = user_context.get('response_to_evaluate', request.query)
            original_query = user_context.get('original_query', '')
            expected_context = user_context.get('expected_context', '')

            # Perform evaluation
            evaluation_result = evaluate_response(
                response=response_to_evaluate,
                original_query=original_query,
                expected_context=expected_context
            )

            # Format the evaluation response
            issues_found = len(evaluation_result.issues)
            quality_percentage = int(evaluation_result.quality_score * 100)

            evaluation_summary = f"EVALUATION RESULTS:\n\n"
            evaluation_summary += f"Quality Score: {quality_percentage}%\n"
            evaluation_summary += f"Issues Found: {issues_found}\n\n"

            if evaluation_result.issues:
                evaluation_summary += "Issues Detected:\n"
                for issue in evaluation_result.issues:
                    evaluation_summary += f"- {issue['type'].title()}: {issue['description']} (Severity: {issue['severity']})\n"
                evaluation_summary += "\n"

            if evaluation_result.suggestions:
                evaluation_summary += "Suggestions for Improvement:\n"
                for suggestion in evaluation_result.suggestions:
                    evaluation_summary += f"- {suggestion}\n"

            if issues_found == 0:
                evaluation_summary += "\nNo significant issues detected. Response appears to be accurate and well-grounded."

            return AgentResponse(
                content=evaluation_summary,
                confidence=evaluation_result.confidence_in_evaluation,
                sources=[f"evaluation_{quality_percentage}_quality"],
                metadata={
                    "agent": self.name,
                    "quality_score": evaluation_result.quality_score,
                    "issues_count": issues_found,
                    "issues": evaluation_result.issues,
                    "suggestions": evaluation_result.suggestions
                }
            )

        except Exception as e:
            logger.error(f"Error processing request in EvaluationAgent: {e}")
            return AgentResponse(
                content="An error occurred while evaluating the response",
                confidence=0.0,
                sources=[],
                metadata={"error": str(e), "agent": self.name}
            )

    def validate_request(self, request: AgentRequest) -> bool:
        """Validate the request, ensuring there's content to evaluate.

        Args:
            request: The request to validate

        Returns:
            True if request is valid, False otherwise
        """
        user_context = request.user_context or {}
        response_to_evaluate = user_context.get('response_to_evaluate', request.query)
        return bool(response_to_evaluate and response_to_evaluate.strip())