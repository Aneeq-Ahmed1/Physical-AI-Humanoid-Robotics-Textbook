#!/usr/bin/env python3
"""
Test script to verify that subagents work properly.
"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_subagents():
    print("Testing subagent imports and basic functionality...")

    try:
        # Test agent router import
        from agent.agent_router import get_router
        print("[OK] Agent router imported successfully")

        # Test base agent import
        from agent.base_agent import AgentRequest, AgentResponse
        print("[OK] Base agent components imported successfully")

        # Test subagent imports
        from agent.subagents.book_expert_agent import BookExpertAgent
        from agent.subagents.selected_text_agent import SelectedTextAgent
        from agent.subagents.chapter_guide_agent import ChapterGuideAgent
        from agent.subagents.evaluation_agent import EvaluationAgent
        print("[OK] All subagent classes imported successfully")

        # Test skill registry
        from agent.skill_registry import list_skills, execute_skill
        print("[OK] Skill registry imported successfully")

        # Test that agents can be instantiated
        book_agent = BookExpertAgent()
        text_agent = SelectedTextAgent()
        chapter_agent = ChapterGuideAgent()
        eval_agent = EvaluationAgent()
        print("[OK] All subagents instantiated successfully")

        # Test that router can register agents
        router = get_router()
        router.register_agent(book_agent)
        router.register_agent(text_agent)
        router.register_agent(chapter_agent)
        router.register_agent(eval_agent)
        print("[OK] All subagents registered with router successfully")

        # Test available skills
        skills = list_skills()
        print(f"[OK] Found {len(skills)} registered skills: {list(skills.keys())}")

        # Test a simple request to each agent
        test_request = AgentRequest(
            query="What is humanoid robotics?",
            user_context={},
            metadata={}
        )

        # Test book expert agent
        book_response = book_agent.process_request(test_request)
        print(f"[OK] Book Expert Agent processed request. Content length: {len(book_response.content) if book_response.content else 0}")

        # Test selected text agent (with selected text in context)
        text_request = AgentRequest(
            query="Explain this concept",
            user_context={"selected_text": "Humanoid robotics is a field of robotics focused on creating robots that resemble humans in form and behavior."},
            metadata={}
        )
        text_response = text_agent.process_request(text_request)
        print(f"[OK] Selected Text Agent processed request. Content length: {len(text_response.content) if text_response.content else 0}")

        # Test chapter guide agent
        chapter_response = chapter_agent.process_request(test_request)
        print(f"[OK] Chapter Guide Agent processed request. Content length: {len(chapter_response.content) if chapter_response.content else 0}")

        # Test evaluation agent
        eval_request = AgentRequest(
            query="Evaluate this response",
            user_context={
                "response_to_evaluate": "This is a sample response for evaluation.",
                "original_query": "What is humanoid robotics?",
            },
            metadata={}
        )
        eval_response = eval_agent.process_request(eval_request)
        print(f"[OK] Evaluation Agent processed request. Content length: {len(eval_response.content) if eval_response.content else 0}")

        print("\n[SUCCESS] All subagent tests passed! The backend components are working properly.")
        return True

    except Exception as e:
        print(f"\n[ERROR] Error during subagent testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_subagents()
    if not success:
        sys.exit(1)