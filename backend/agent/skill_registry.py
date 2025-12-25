from typing import Any, Callable, Dict, Optional
from functools import wraps


# Global registry for skills
_SKILL_REGISTRY: Dict[str, Callable] = {}


def register_skill(
    skill_id: str,
    name: str = "",
    description: str = "",
    input_schema: Optional[Dict] = None,
    output_schema: Optional[Dict] = None
):
    """Decorator to register a skill in the skill registry.

    Args:
        skill_id: Unique identifier for the skill
        name: Human-readable name of the skill
        description: Description of what the skill does
        input_schema: JSON schema defining expected input parameters
        output_schema: JSON schema defining expected output format
    """
    def decorator(func: Callable) -> Callable:
        skill_info = {
            'function': func,
            'name': name or func.__name__,
            'description': description or func.__doc__ or "",
            'input_schema': input_schema or {},
            'output_schema': output_schema or {},
            'callable': func
        }
        _SKILL_REGISTRY[skill_id] = skill_info
        return func
    return decorator


def get_skill(skill_id: str) -> Optional[Callable]:
    """Get a skill function by its ID.

    Args:
        skill_id: ID of the skill to retrieve

    Returns:
        Callable skill function or None if not found
    """
    skill_info = _SKILL_REGISTRY.get(skill_id)
    return skill_info['callable'] if skill_info else None


def get_skill_info(skill_id: str) -> Optional[Dict]:
    """Get detailed information about a skill.

    Args:
        skill_id: ID of the skill to retrieve info for

    Returns:
        Dictionary with skill information or None if not found
    """
    return _SKILL_REGISTRY.get(skill_id)


def list_skills() -> Dict[str, Dict]:
    """List all registered skills with their information.

    Returns:
        Dictionary mapping skill IDs to their information
    """
    return {skill_id: {
        'name': info['name'],
        'description': info['description'],
        'input_schema': info['input_schema'],
        'output_schema': info['output_schema']
    } for skill_id, info in _SKILL_REGISTRY.items()}


def execute_skill(skill_id: str, **kwargs) -> Any:
    """Execute a skill with the given parameters.

    Args:
        skill_id: ID of the skill to execute
        **kwargs: Parameters to pass to the skill

    Returns:
        Result of the skill execution

    Raises:
        ValueError: If skill is not found
        Exception: If skill execution fails
    """
    skill_func = get_skill(skill_id)
    if skill_func is None:
        raise ValueError(f"Skill '{skill_id}' not found")
    return skill_func(**kwargs)


# Example skill implementations (will be replaced by actual implementations in other files)
@register_skill(
    skill_id="retrieve_book_chunks",
    name="Retrieve Book Chunks",
    description="Retrieve relevant chunks of text from the book based on the query"
)
def retrieve_book_chunks(query: str, max_chunks: int = 5, **kwargs) -> list:
    """Example implementation - will be replaced with actual RAG functionality."""
    # This is a placeholder - actual implementation would connect to RAG system
    return [{"content": f"Sample chunk related to: {query}", "source": "sample_source"}]


@register_skill(
    skill_id="answer_from_selected_text",
    name="Answer from Selected Text",
    description="Answer questions based only on the provided text, without external context"
)
def answer_from_selected_text(selected_text: str, question: str, **kwargs) -> str:
    """Example implementation - will be replaced with actual text analysis."""
    # This is a placeholder - actual implementation would analyze the text
    return f"Based on the selected text: '{selected_text[:50]}...', the answer to '{question}' is computed from the provided text only."


@register_skill(
    skill_id="summarize_chapter",
    name="Summarize Chapter",
    description="Create a summary of a specific chapter"
)
def summarize_chapter(chapter_content: str, **kwargs) -> str:
    """Example implementation - will be replaced with actual summarization."""
    # This is a placeholder - actual implementation would summarize the chapter
    return f"Summary of chapter: {chapter_content[:100]}..."


@register_skill(
    skill_id="explain_like_five",
    name="Explain Like Five",
    description="Explain a concept in simple terms as if explaining to a 5-year-old"
)
def explain_like_five(concept: str, **kwargs) -> str:
    """Example implementation - will be replaced with actual simplification logic."""
    # This is a placeholder - actual implementation would simplify the concept
    return f"Simple explanation of '{concept}': This is a very simplified explanation for a young child."