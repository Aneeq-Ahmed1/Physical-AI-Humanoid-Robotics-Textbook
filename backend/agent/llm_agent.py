import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from .gemini_openai_wrapper import OpenAIGeminiClient

load_dotenv()

class LLMAgent:
    def __init__(self):
        # Configure OpenAI client to use Google's Gemini API through wrapper
        self.client = OpenAIGeminiClient(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "gemini-2.5-flash"  # Using latest available Gemini model

    def generate_response_full_rag(self, query: str, context_documents: List[Dict[str, Any]]) -> str:
        """
        Generate response using full-book RAG mode with retrieved documents as context
        """
        if not context_documents:
            # Handle case where no documents were retrieved
            messages = [
                {
                    "role": "system",
                    "content": "You are an expert assistant for the Humanoid Robotics textbook."
                },
                {
                    "role": "user",
                    "content": f"""
                    I couldn't find specific information about your question in the textbook content.

                    Question: {query}

                    Please acknowledge that you don't have specific information from the textbook about this topic,
                    but if you have general knowledge about humanoid robotics that could be helpful,
                    you may provide that information while clearly stating it's general knowledge
                    and not from the specific textbook content.
                    """
                }
            ]
        else:
            # Format the context from retrieved documents
            context = "\n\n".join([doc["text"] for doc in context_documents])

            messages = [
                {
                    "role": "system",
                    "content": "You are an expert assistant for the Humanoid Robotics textbook. Answer the user's question based on the provided context from the book."
                },
                {
                    "role": "user",
                    "content": f"""
                    Context: {context}

                    Question: {query}

                    Please provide a comprehensive answer based on the context, citing the relevant sources.
                    If the answer cannot be found in the provided context, politely inform the user.
                    """
                }
            ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.3  # Low temperature for factual accuracy
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating response with Gemini: {e}")
            # Return a more descriptive error that can help with debugging
            error_msg = f"I encountered an error while processing your request. Error details: {str(e)}. Please check your Gemini API key and ensure the backend is running properly."
            return error_msg

    def generate_response_selected_text(self, query: str, selected_text: str) -> str:
        """
        Generate response using selected-text-only mode, strictly using only the provided text
        """
        messages = [
            {
                "role": "system",
                "content": "You are an expert assistant for the Humanoid Robotics textbook. Answer the user's question based ONLY on the selected text provided. Do not use any external knowledge or information beyond what's in the selected text."
            },
            {
                "role": "user",
                "content": f"""
                Selected Text: {selected_text}

                Question: {query}

                Please provide an answer based only on the selected text.
                """
            }
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.3  # Low temperature for factual accuracy
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating response with Gemini: {e}")
            # Return a more descriptive error that can help with debugging
            error_msg = f"I encountered an error while processing your request. Error details: {str(e)}. Please check your Gemini API key and ensure the backend is running properly."
            return error_msg