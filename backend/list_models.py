#!/usr/bin/env python3
"""
Script to list available Gemini models
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def list_available_models():
    """List all available models from the Gemini API"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        print("Please set a valid GEMINI_API_KEY in your .env file")
        return

    genai.configure(api_key=api_key)

    print("Available models:")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"  - {model.name}")

if __name__ == "__main__":
    list_available_models()