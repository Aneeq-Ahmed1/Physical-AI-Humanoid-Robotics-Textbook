"""Simple test script for personalization functionality."""

import sys
import os
# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from agent.subagents.chapter_guide_agent import ChapterGuideAgent
from agent.base_agent import AgentRequest
from api.personalization_cache import personalization_cache
import uuid


def simple_test():
    """Simple test of personalization functionality."""
    print("Testing personalization functionality...")

    chapter_content = """
# Introduction to Humanoid Robotics

Humanoid robots are robots that resemble humans in form and behavior.
They typically have a head, torso, two arms, and two legs, though some
designs may vary. The development of humanoid robots involves multiple
disciplines including mechanical engineering, electrical engineering,
computer science, and artificial intelligence.
"""

    print("1. Testing Chapter Guide Agent with different difficulty levels...")

    # Test beginner level
    agent = ChapterGuideAgent()
    beginner_request = AgentRequest(
        query=chapter_content,
        user_context={
            "difficulty_preference": "beginner",
            "chapter": "intro-humanoid-robotics",
            "chapter_content": chapter_content
        }
    )
    beginner_response = agent.process_request(beginner_request)
    print(f"   ✓ Beginner content generated: {len(beginner_response.content)} chars")

    # Test intermediate level
    intermediate_request = AgentRequest(
        query=chapter_content,
        user_context={
            "difficulty_preference": "intermediate",
            "chapter": "intro-humanoid-robotics",
            "chapter_content": chapter_content
        }
    )
    intermediate_response = agent.process_request(intermediate_request)
    print(f"   ✓ Intermediate content generated: {len(intermediate_response.content)} chars")

    # Test advanced level
    advanced_request = AgentRequest(
        query=chapter_content,
        user_context={
            "difficulty_preference": "advanced",
            "chapter": "intro-humanoid-robotics",
            "chapter_content": chapter_content
        }
    )
    advanced_response = agent.process_request(advanced_request)
    print(f"   ✓ Advanced content generated: {len(advanced_response.content)} chars")

    print("\n2. Testing session caching...")

    # Create a session
    session_id = f"test_session_{uuid.uuid4()}"
    session = personalization_cache.create_session(
        session_id=session_id,
        difficulty_level="intermediate",
        original_content=chapter_content,
        chapter_id="intro-humanoid-robotics"
    )

    if session:
        print(f"   ✓ Session created: {session.session_id}")

        # Update content in cache
        success = personalization_cache.update_session_content(
            session_id,
            "Test personalized content"
        )
        if success:
            print(f"   ✓ Content updated in cache")

            # Retrieve session
            retrieved_session = personalization_cache.get_session(session_id)
            if retrieved_session:
                print(f"   ✓ Session retrieved from cache")
            else:
                print(f"   ✗ Session not retrieved from cache")
                return False
        else:
            print(f"   ✗ Failed to update content in cache")
            return False
    else:
        print(f"   ✗ Session creation failed")
        return False

    print("\n✓ All tests passed!")
    return True


if __name__ == "__main__":
    success = simple_test()
    if success:
        print("\n🎉 Personalization functionality test completed successfully!")
    else:
        print("\n❌ Personalization functionality test failed!")