"""Data models for the personalization feature."""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class DifficultyLevel(str, Enum):
    """Enumeration of available difficulty levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class PersonalizationSession:
    """Represents a personalization session with user preferences and cached content."""

    session_id: str
    difficulty_level: str
    original_content: str
    personalized_content: str
    chapter_id: str
    created_at: float
    last_accessed: float
    reading_position: int = 0


@dataclass
class PersonalizationPreferences:
    """User preferences for content personalization."""

    difficulty_level: DifficultyLevel
    reading_position: int = 0
    preferred_format: str = "text"  # Could be 'text', 'visual', 'audio', etc.
    content_focus: Optional[str] = None  # Specific topic focus if any