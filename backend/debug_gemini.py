#!/usr/bin/env python3
"""
Debug script to test Gemini API functionality directly
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def test_gemini_api_directly():
    """Test Gemini API directly without the wrapper to isolate the issue"""
    print("Testing Gemini API directly...")

    try:
        import google.generativeai as genai

        # Get API key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
            print("[ERROR] No valid GEMINI_API_KEY found in environment.")
            print("Please add your actual Gemini API key to the .env file.")
            return False

        # Configure the API
        genai.configure(api_key=api_key)

        # Create a model instance
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Test a simple prompt
        test_prompt = "Hello, how are you? Just respond with 'API working' if you can process this."

        print("Sending test request to Gemini API...")
        response = model.generate_content(
            test_prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=100,
                temperature=0.3
            ),
            safety_settings={
                "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
            }
        )

        if response.text:
            print(f"[SUCCESS] Gemini API is working! Response: {response.text}")
            return True
        else:
            print("[ERROR] Gemini API returned empty response")
            return False

    except Exception as e:
        print(f"[ERROR] Gemini API direct test failed: {e}")
        return False

def test_gemini_wrapper():
    """Test the wrapper functionality"""
    print("\nTesting Gemini wrapper...")

    try:
        from agent.gemini_openai_wrapper import OpenAIGeminiClient

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
            print("[ERROR] No valid GEMINI_API_KEY found in environment.")
            return False

        # Create client using wrapper
        client = OpenAIGeminiClient(api_key=api_key)

        # Test the chat completion
        test_messages = [
            {
                "role": "user",
                "content": "Hello, how are you? Just respond with 'Wrapper working' if you can process this."
            }
        ]

        print("Testing wrapper chat completion...")
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=test_messages,
            max_tokens=100,
            temperature=0.3
        )

        if response.choices and response.choices[0].message.content:
            print(f"[SUCCESS] Wrapper is working! Response: {response.choices[0].message.content}")
            return True
        else:
            print("[ERROR] Wrapper returned empty response")
            return False

    except Exception as e:
        print(f"[ERROR] Gemini wrapper test failed: {e}")
        return False

def test_llm_agent():
    """Test the full LLM agent"""
    print("\nTesting LLM agent...")

    try:
        from agent.llm_agent import LLMAgent

        agent = LLMAgent()

        # Test a simple response generation
        test_query = "Hello, how are you?"
        test_context = []

        print("Testing LLM agent response generation...")
        response = agent.generate_response_full_rag(test_query, test_context)

        if "encountered an error" not in response.lower():
            print(f"[SUCCESS] LLM agent is working! Response: {response}")
            return True
        else:
            print(f"[ERROR] LLM agent failed: {response}")
            return False

    except Exception as e:
        print(f"[ERROR] LLM agent test failed: {e}")
        return False

def main():
    print("Running Gemini API debug tests...\n")

    success = True
    success &= test_gemini_api_directly()
    success &= test_gemini_wrapper()
    success &= test_llm_agent()

    print(f"\n{'='*60}")
    if success:
        print("[SUCCESS] All tests passed! The Gemini API integration should work.")
        print("\nMake sure your backend is running with: uvicorn main:app --reload")
        print("Then try the chatbot again.")
    else:
        print("[FAILURE] Some tests failed. Please check the errors above.")
        print("\nCommon issues:")
        print("1. Invalid or expired GEMINI_API_KEY")
        print("2. Network connectivity issues")
        print("3. Rate limiting from Google")
        print("4. Incorrect model name")

    return success

if __name__ == "__main__":
    main()