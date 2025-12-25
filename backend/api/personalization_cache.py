"""Session-based caching mechanism for personalization."""

import time
from typing import Dict, Optional, Any
from threading import Lock
try:
    # When running as part of the backend package
    from ..agent.models import PersonalizationSession
except (ValueError, ImportError):
    # When running directly for testing
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    try:
        from agent.models import PersonalizationSession
    except ImportError:
        # If direct import fails, try absolute import
        from backend.agent.models import PersonalizationSession


class PersonalizationCache:
    """Thread-safe in-memory cache for personalization sessions."""

    def __init__(self, ttl_seconds: int = 3600):  # 1 hour default TTL
        self._cache: Dict[str, PersonalizationSession] = {}
        self._lock = Lock()
        self._ttl_seconds = ttl_seconds

    def get_session(self, session_id: str) -> Optional[PersonalizationSession]:
        """Get a personalization session by ID, or None if not found or expired."""
        with self._lock:
            if session_id in self._cache:
                session = self._cache[session_id]
                # Check if session has expired
                if time.time() - session.last_accessed > self._ttl_seconds:
                    del self._cache[session_id]
                    return None
                # Update last accessed time
                session.last_accessed = time.time()
                return session
            return None

    def cleanup_expired_sessions(self):
        """Remove all expired sessions from the cache."""
        with self._lock:
            current_time = time.time()
            expired_sessions = [
                sid for sid, session in self._cache.items()
                if current_time - session.last_accessed > self._ttl_seconds
            ]
            for sid in expired_sessions:
                del self._cache[sid]
            return len(expired_sessions)

    def create_session(self, session_id: str, difficulty_level: str, original_content: str,
                      chapter_id: str, reading_position: int = 0) -> PersonalizationSession:
        """Create a new personalization session."""
        with self._lock:
            created_at = time.time()
            session = PersonalizationSession(
                session_id=session_id,
                difficulty_level=difficulty_level,
                original_content=original_content,
                personalized_content="",  # Will be set later
                chapter_id=chapter_id,
                created_at=created_at,
                last_accessed=created_at,
                reading_position=reading_position
            )
            self._cache[session_id] = session
            return session

    def update_session_content(self, session_id: str, personalized_content: str) -> bool:
        """Update the personalized content for a session."""
        with self._lock:
            if session_id in self._cache:
                session = self._cache[session_id]
                session.personalized_content = personalized_content
                session.last_accessed = time.time()
                return True
            return False

    def update_reading_position(self, session_id: str, position: int) -> bool:
        """Update the reading position for a session."""
        with self._lock:
            if session_id in self._cache:
                session = self._cache[session_id]
                session.reading_position = position
                session.last_accessed = time.time()
                return True
            return False

    def update_difficulty_level(self, session_id: str, difficulty_level: str) -> bool:
        """Update the difficulty level for a session."""
        with self._lock:
            if session_id in self._cache:
                session = self._cache[session_id]
                session.difficulty_level = difficulty_level
                session.last_accessed = time.time()
                return True
            return False

    def clear_session(self, session_id: str) -> bool:
        """Remove a session from the cache."""
        with self._lock:
            if session_id in self._cache:
                del self._cache[session_id]
                return True
            return False


# Global instance
personalization_cache = PersonalizationCache()