from ..skill_registry import register_skill
from typing import List, Dict, Any, Optional
import logging


logger = logging.getLogger(__name__)


@register_skill(
    skill_id="answer_from_selected_text",
    name="Answer from Selected Text",
    description="Answer questions based only on the provided text, without external context",
    input_schema={
        "type": "object",
        "properties": {
            "selected_text": {"type": "string", "description": "The specific text to analyze"},
            "question": {"type": "string", "description": "The question about the selected text"}
        },
        "required": ["selected_text", "question"]
    },
    output_schema={
        "type": "string"
    }
)
def answer_from_selected_text(selected_text: str, question: str, **kwargs) -> str:
    """Answer questions based only on the provided text, without external context.

    Args:
        selected_text: The specific text to analyze
        question: The question about the selected text
        **kwargs: Additional parameters

    Returns:
        Answer based only on the provided text
    """
    try:
        # Connect to the LLM to generate an answer based only on the selected text
        from ...agent.llm_agent import LLMAgent

        llm_agent = LLMAgent()

        # Create a message to send to the LLM that specifically asks it to use only the provided text
        response = llm_agent.generate_response_selected_text(
            query=question,
            selected_text=selected_text
        )

        return response
    except Exception as e:
        logger.error(f"Error in answer_from_selected_text skill: {e}")
        return f"Error processing the selected text: {str(e)}"


@register_skill(
    skill_id="analyze_text_complexity",
    name="Analyze Text Complexity",
    description="Analyze the complexity level of the provided text",
    input_schema={
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "The text to analyze for complexity"}
        },
        "required": ["text"]
    },
    output_schema={
        "type": "object",
        "properties": {
            "complexity_level": {"type": "string", "enum": ["beginner", "intermediate", "advanced"]},
            "readability_score": {"type": "number"},
            "estimated_grade_level": {"type": "number"}
        }
    }
)
def analyze_text_complexity(text: str, **kwargs) -> Dict[str, Any]:
    """Analyze the complexity level of the provided text.

    Args:
        text: The text to analyze for complexity
        **kwargs: Additional parameters

    Returns:
        Dictionary containing complexity analysis
    """
    try:
        # This is a simplified implementation
        # In a real system, this would use sophisticated NLP metrics
        word_count = len(text.split())
        avg_word_length = sum(len(word) for word in text.split()) / max(1, word_count)

        if avg_word_length < 4:
            complexity_level = "beginner"
        elif avg_word_length < 6:
            complexity_level = "intermediate"
        else:
            complexity_level = "advanced"

        return {
            "complexity_level": complexity_level,
            "readability_score": min(1.0, word_count / 1000),  # Simplified score
            "estimated_grade_level": 8 if complexity_level == "beginner" else (12 if complexity_level == "intermediate" else 16)
        }
    except Exception as e:
        logger.error(f"Error in analyze_text_complexity skill: {e}")
        return {
            "complexity_level": "intermediate",
            "readability_score": 0.5,
            "estimated_grade_level": 12
        }


@register_skill(
    skill_id="extract_key_points",
    name="Extract Key Points",
    description="Extract key points from the provided text",
    input_schema={
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "The text to extract key points from"}
        },
        "required": ["text"]
    },
    output_schema={
        "type": "array",
        "items": {"type": "string"}
    }
)
def extract_key_points(text: str, **kwargs) -> List[str]:
    """Extract key points from the provided text.

    Args:
        text: The text to extract key points from
        **kwargs: Additional parameters

    Returns:
        List of key points extracted from the text
    """
    try:
        # This is a simplified implementation
        # In a real system, this would use NLP techniques to identify key points
        sentences = text.split('.')
        # Take the first few sentences as key points (simplified approach)
        key_points = [s.strip() for s in sentences[:3] if len(s.strip()) > 10]

        if not key_points:
            key_points = ["Key points could not be extracted from the provided text"]

        return key_points
    except Exception as e:
        logger.error(f"Error in extract_key_points skill: {e}")
        return ["Error extracting key points"]