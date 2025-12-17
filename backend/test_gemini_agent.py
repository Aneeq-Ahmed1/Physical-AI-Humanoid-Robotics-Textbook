#!/usr/bin/env python3
"""
Simple test to verify the Gemini agent is properly configured
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def test_gemini_agent():
    """Test that the Gemini agent can be initialized properly"""
    print("Testing Gemini agent initialization...")

    try:
        from agent.llm_agent import LLMAgent
        agent = LLMAgent()
        print("[OK] Gemini agent initialized successfully")

        # Check if API key is set
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key and api_key != "YOUR_GEMINI_API_KEY_HERE":
            print("[OK] GEMINI_API_KEY is set in environment")
            return True
        else:
            print("[WARNING] GEMINI_API_KEY is not set. Please add your actual Gemini API key to the .env file.")
            print("You can get one from: https://aistudio.google.com/app/apikey")
            return False

    except Exception as e:
        print(f"[ERROR] Failed to initialize Gemini agent: {e}")
        return False

def test_gemini_wrapper():
    """Test that the Gemini wrapper is working properly"""
    print("\nTesting Gemini wrapper...")

    try:
        from agent.gemini_openai_wrapper import OpenAIGeminiClient
        api_key = os.getenv("GEMINI_API_KEY")

        if api_key and api_key != "YOUR_GEMINI_API_KEY_HERE":
            client = OpenAIGeminiClient(api_key=api_key)
            print("[OK] Gemini wrapper initialized successfully")
        else:
            print("[INFO] Skipping wrapper functionality test - no API key provided")

        return True
    except Exception as e:
        print(f"[ERROR] Failed to initialize Gemini wrapper: {e}")
        return False

def main():
    print("Running Gemini API configuration tests...\n")

    success = True
    success &= test_gemini_agent()
    success &= test_gemini_wrapper()

    print(f"\n{'='*50}")
    if success:
        print("[OK] All Gemini configuration tests passed!")
        print("\nTo use the chatbot:")
        print("1. Make sure you have a valid GEMINI_API_KEY in your .env file")
        print("2. Run the backend with: uvicorn main:app --reload")
        print("3. Start the Docusaurus frontend")
        print("4. The chatbot should now work with Gemini API via OpenAI SDK")
    else:
        print("[ERROR] Some tests failed. Please check the errors above.")

    return success

if __name__ == "__main__":
    main()