from ..skill_registry import register_skill
from ..evaluation import evaluate_response, EvaluationResult
from typing import List, Dict, Any, Optional
import logging


logger = logging.getLogger(__name__)


@register_skill(
    skill_id="hallucination_detection",
    name="Hallucination Detection",
    description="Detect hallucinations in AI-generated responses",
    input_schema={
        "type": "object",
        "properties": {
            "response": {"type": "string", "description": "The response to check for hallucinations"},
            "context": {"type": "string", "description": "The context or source material for verification"}
        },
        "required": ["response"]
    },
    output_schema={
        "type": "object",
        "properties": {
            "has_hallucination": {"type": "boolean"},
            "confidence": {"type": "number"},
            "details": {"type": "string"}
        }
    }
)
def hallucination_detection(response: str, context: Optional[str] = None, **kwargs) -> Dict[str, Any]:
    """Detect hallucinations in AI-generated responses.

    Args:
        response: The response to check for hallucinations
        context: The context or source material for verification (optional)
        **kwargs: Additional parameters

    Returns:
        Dictionary with hallucination detection results
    """
    try:
        # This is a simplified implementation
        # In a real system, this would connect to a fact-checking system or knowledge base
        # For now, we'll look for common hallucination patterns

        hallucination_indicators = [
            "was born on [date]",  # Placeholder dates
            "according to page [number]",  # Placeholder page references
            "as mentioned in chapter [number]",  # Placeholder chapter references
            "cited in [source]",  # Unverifiable sources
        ]

        has_hallucination = False
        details = []

        response_lower = response.lower()
        for indicator in hallucination_indicators:
            if indicator.replace("[date]", "").replace("[number]", "").replace("[source]", "") in response_lower:
                has_hallucination = True
                details.append(f"Potential hallucination detected: {indicator}")

        # If context is provided, check for consistency
        if context:
            # This is a simplified check - in reality would need semantic comparison
            if len(response) > len(context) * 2 and "according to" in response_lower:
                has_hallucination = True
                details.append("Response contains claims not supported by the provided context")

        confidence = 0.8 if has_hallucination else 0.95

        return {
            "has_hallucination": has_hallucination,
            "confidence": confidence,
            "details": " ".join(details) if details else "No hallucinations detected"
        }
    except Exception as e:
        logger.error(f"Error in hallucination_detection skill: {e}")
        return {
            "has_hallucination": False,
            "confidence": 0.5,
            "details": f"Error during hallucination detection: {str(e)}"
        }


@register_skill(
    skill_id="response_quality_check",
    name="Response Quality Check",
    description="Comprehensive quality check of AI-generated responses",
    input_schema={
        "type": "object",
        "properties": {
            "response": {"type": "string", "description": "The response to evaluate"},
            "query": {"type": "string", "description": "The original query"},
            "context": {"type": "string", "description": "The context provided to generate the response"}
        },
        "required": ["response", "query"]
    },
    output_schema={
        "type": "object",
        "properties": {
            "quality_score": {"type": "number"},
            "issues": {"type": "array", "items": {"type": "string"}},
            "suggestions": {"type": "array", "items": {"type": "string"}}
        }
    }
)
def response_quality_check(response: str, query: str, context: Optional[str] = None, **kwargs) -> Dict[str, Any]:
    """Comprehensive quality check of AI-generated responses.

    Args:
        response: The response to evaluate
        query: The original query
        context: The context provided to generate the response (optional)
        **kwargs: Additional parameters

    Returns:
        Dictionary with quality assessment results
    """
    try:
        # Use the evaluation framework to get a comprehensive evaluation
        evaluation_result = evaluate_response(
            response=response,
            original_query=query,
            expected_context=context
        )

        return {
            "quality_score": evaluation_result.quality_score,
            "issues": [f"{issue['type']}: {issue['description']}" for issue in evaluation_result.issues],
            "suggestions": evaluation_result.suggestions
        }
    except Exception as e:
        logger.error(f"Error in response_quality_check skill: {e}")
        return {
            "quality_score": 0.5,
            "issues": [f"Error during quality check: {str(e)}"],
            "suggestions": ["Unable to perform quality check due to an error"]
        }


@register_skill(
    skill_id="source_consistency_check",
    name="Source Consistency Check",
    description="Check if the response is consistent with provided sources",
    input_schema={
        "type": "object",
        "properties": {
            "response": {"type": "string", "description": "The response to check"},
            "sources": {"type": "array", "items": {"type": "string"}, "description": "List of source materials"}
        },
        "required": ["response", "sources"]
    },
    output_schema={
        "type": "object",
        "properties": {
            "is_consistent": {"type": "boolean"},
            "confidence": {"type": "number"},
            "inconsistencies": {"type": "array", "items": {"type": "string"}}
        }
    }
)
def source_consistency_check(response: str, sources: List[str], **kwargs) -> Dict[str, Any]:
    """Check if the response is consistent with provided sources.

    Args:
        response: The response to check
        sources: List of source materials
        **kwargs: Additional parameters

    Returns:
        Dictionary with consistency check results
    """
    try:
        # This is a simplified implementation
        # In a real system, this would use semantic similarity checks
        is_consistent = True
        inconsistencies = []

        # Simple keyword-based consistency check
        combined_sources = " ".join(sources).lower()
        response_lower = response.lower()

        # Look for claims in response that aren't supported by sources
        if "according to" in response_lower and not any(source.lower() in combined_sources for source in sources):
            is_consistent = False
            inconsistencies.append("Response references sources not found in provided materials")

        confidence = 0.8 if is_consistent else 0.3

        return {
            "is_consistent": is_consistent,
            "confidence": confidence,
            "inconsistencies": inconsistencies
        }
    except Exception as e:
        logger.error(f"Error in source_consistency_check skill: {e}")
        return {
            "is_consistent": False,
            "confidence": 0.5,
            "inconsistencies": [f"Error during consistency check: {str(e)}"]
        }