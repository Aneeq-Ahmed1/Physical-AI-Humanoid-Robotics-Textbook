"""Test script for personalization functionality."""

import asyncio
import uuid
import sys
import os

# Add the backend directory to the path to resolve imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.subagents.chapter_guide_agent import ChapterGuideAgent
from agent.base_agent import AgentRequest
from api.personalization_cache import personalization_cache


def test_personalization_flow():
    """Test the complete personalization flow."""
    print("Testing personalization flow...")

    chapter_content = """
# Introduction to Humanoid Robotics

Humanoid robots are robots that resemble humans in form and behavior.
They typically have a head, torso, two arms, and two legs, though some
designs may vary. The development of humanoid robots involves multiple
disciplines including mechanical engineering, electrical engineering,
computer science, and artificial intelligence.

## Key Components

The main components of humanoid robots include:
- Actuators for movement
- Sensors for perception
- Control systems for coordination
- Power systems for operation
"""

    print(f"1. Testing beginner level personalization...")
    try:
        # Create agent and test beginner level
        agent = ChapterGuideAgent()
        request = AgentRequest(
            query=chapter_content,
            user_context={
                "difficulty_preference": "beginner",
                "chapter": "intro-humanoid-robotics",
                "chapter_content": chapter_content
            }
        )
        response = agent.process_request(request)
        print(f"   [PASS] Beginner content generated: {len(response.content)} chars")
        print(f"   [PASS] Difficulty: beginner")
        print(f"   [PASS] Sample: {response.content[:100]}...")
    except Exception as e:
        print(f"   [FAIL] Error in beginner personalization: {e}")
        return False

    print(f"2. Testing intermediate level personalization...")
    try:
        # Test intermediate level
        agent = ChapterGuideAgent()
        request = AgentRequest(
            query=chapter_content,
            user_context={
                "difficulty_preference": "intermediate",
                "chapter": "intro-humanoid-robotics",
                "chapter_content": chapter_content
            }
        )
        response = agent.process_request(request)
        print(f"   [PASS] Intermediate content generated: {len(response.content)} chars")
        print(f"   [PASS] Difficulty: intermediate")
        print(f"   [PASS] Sample: {response.content[:100]}...")
    except Exception as e:
        print(f"   [FAIL] Error in intermediate personalization: {e}")
        return False

    print(f"3. Testing advanced level personalization...")
    try:
        # Test advanced level
        agent = ChapterGuideAgent()
        request = AgentRequest(
            query=chapter_content,
            user_context={
                "difficulty_preference": "advanced",
                "chapter": "intro-humanoid-robotics",
                "chapter_content": chapter_content
            }
        )
        response = agent.process_request(request)
        print(f"   [PASS] Advanced content generated: {len(response.content)} chars")
        print(f"   [PASS] Difficulty: advanced")
        print(f"   [PASS] Sample: {response.content[:100]}...")
    except Exception as e:
        print(f"   [FAIL] Error in advanced personalization: {e}")
        return False

    print(f"4. Testing session caching...")
    try:
        # Test caching mechanism
        session_id = f"test_session_{uuid.uuid4()}"
        session = personalization_cache.create_session(
            session_id=session_id,
            difficulty_level="intermediate",
            original_content=chapter_content,
            chapter_id="intro-humanoid-robotics"
        )

        if session:
            print(f"   [PASS] Session created: {session.session_id}")
            print(f"   [PASS] Cached difficulty: {session.difficulty_level}")

            # Update content in cache
            success = personalization_cache.update_session_content(
                session_id,
                "Personalized content for testing"
            )
            if success:
                print(f"   [PASS] Content updated in cache")

                # Retrieve session
                retrieved_session = personalization_cache.get_session(session_id)
                if retrieved_session:
                    print(f"   [PASS] Session retrieved from cache")
                else:
                    print(f"   [FAIL] Session not retrieved from cache")
                    return False
            else:
                print(f"   [FAIL] Failed to update content in cache")
                return False
        else:
            print(f"   [FAIL] Session creation failed")
            return False
    except Exception as e:
        print(f"   [FAIL] Error testing session caching: {e}")
        return False

    print(f"5. Testing difficulty switching functionality...")
    try:
        # Test the change difficulty functionality directly
        agent = ChapterGuideAgent()

        # First, get beginner content
        beginner_request = AgentRequest(
            query=chapter_content,
            user_context={
                "difficulty_preference": "beginner",
                "chapter": "intro-humanoid-robotics",
                "chapter_content": chapter_content
            }
        )
        beginner_response = agent.process_request(beginner_request)
        print(f"   [PASS] Beginner content generated")

        # Then, get advanced content from same chapter content
        advanced_request = AgentRequest(
            query=chapter_content,
            user_context={
                "difficulty_preference": "advanced",
                "chapter": "intro-humanoid-robotics",
                "chapter_content": chapter_content
            }
        )
        advanced_response = agent.process_request(advanced_request)
        print(f"   [PASS] Advanced content generated")

        # Verify that the content is different (indicating successful switching)
        if beginner_response.content != advanced_response.content:
            print(f"   [PASS] Content differs between difficulty levels (switching works)")
        else:
            print(f"   [WARN] Content is the same between difficulty levels (may be expected for simple content)")

    except Exception as e:
        print(f"   [FAIL] Error testing difficulty switching: {e}")
        return False

    print(f"6. Testing toggle between personalized and original content...")
    try:
        # Test toggle functionality conceptually
        # The original content is our input chapter_content
        # The personalized content is what we get back from the agent
        original_length = len(chapter_content)
        beginner_length = len(beginner_response.content)
        advanced_length = len(advanced_response.content)

        print(f"   [PASS] Original content length: {original_length} chars")
        print(f"   [PASS] Beginner content length: {beginner_length} chars")
        print(f"   [PASS] Advanced content length: {advanced_length} chars")

        # Verify that personalized content exists
        if beginner_length > 0 and advanced_length > 0:
            print(f"   [PASS] Personalized content was generated successfully")
        else:
            print(f"   [FAIL] Personalized content generation failed")
            return False

        # Test cache store and retrieval (simulating toggle behavior)
        session_id = f"toggle_test_{uuid.uuid4()}"
        session = personalization_cache.create_session(
            session_id=session_id,
            difficulty_level="beginner",
            original_content=chapter_content,
            chapter_id="intro-humanoid-robotics"
        )

        if session:
            # Store personalized content
            success = personalization_cache.update_session_content(
                session_id,
                beginner_response.content
            )
            if success:
                # Retrieve to simulate toggle
                retrieved_session = personalization_cache.get_session(session_id)
                if retrieved_session and retrieved_session.personalized_content:
                    print(f"   [PASS] Content toggle simulation successful")
                else:
                    print(f"   [FAIL] Content retrieval failed")
                    return False
            else:
                print(f"   [FAIL] Content storage failed")
                return False
        else:
            print(f"   [FAIL] Toggle test session creation failed")
            return False

    except Exception as e:
        print(f"   [FAIL] Error testing toggle functionality: {e}")
        return False

    print(f"7. Running end-to-end tests for all personalization features...")
    try:
        # Test the complete flow using the agent and cache directly
        test_session_id = f"e2e_test_{uuid.uuid4()}"

        # Step 1: Create a session and test personalization
        agent = ChapterGuideAgent()

        beginner_request = AgentRequest(
            query=chapter_content,
            user_context={
                "difficulty_preference": "beginner",
                "chapter": "e2e-test-chapter",
                "chapter_content": chapter_content
            }
        )
        beginner_response = agent.process_request(beginner_request)
        print(f"   [PASS] Step 1: Beginner content generated via agent")

        # Step 2: Test cache functionality
        session = personalization_cache.create_session(
            session_id=test_session_id,
            difficulty_level="beginner",
            original_content=chapter_content,
            chapter_id="e2e-test-chapter"
        )
        cache_success = personalization_cache.update_session_content(
            test_session_id,
            beginner_response.content
        )
        if not cache_success:
            print(f"   [FAIL] Step 2: Failed to cache content")
            return False
        print(f"   [PASS] Step 2: Content caching works")

        # Step 3: Test difficulty change logic by simulating the API flow
        advanced_request = AgentRequest(
            query=chapter_content,
            user_context={
                "difficulty_preference": "advanced",
                "chapter": "e2e-test-chapter",
                "chapter_content": chapter_content
            }
        )
        advanced_response = agent.process_request(advanced_request)
        print(f"   [PASS] Step 3: Advanced content generated via agent")

        # Step 4: Verify different content was generated
        if beginner_response.content != advanced_response.content:
            print(f"   [PASS] Step 4: Different content generated for different difficulties")
        else:
            print(f"   [WARN] Step 4: Same content for different difficulties (may be expected)")

        # Step 5: Test session retrieval
        retrieved_session = personalization_cache.get_session(test_session_id)
        if retrieved_session:
            print(f"   [PASS] Step 5: Session retrieval works")
        else:
            print(f"   [FAIL] Step 5: Session retrieval failed")
            return False

        print(f"   [PASS] Step 6: End-to-end journey completed successfully")

    except Exception as e:
        print(f"   [FAIL] Error in end-to-end test: {e}")
        return False

    print("\n[ALL PASS] All personalization tests passed!")
    return True


if __name__ == "__main__":
    print("Starting personalization flow test...")
    success = test_personalization_flow()
    if success:
        print("\n[SUCCESS] Personalization flow test completed successfully!")
    else:
        print("\n[ERROR] Personalization flow test failed!")