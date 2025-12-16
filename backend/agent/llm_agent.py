import os
import cohere
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class LLMAgent:
    def __init__(self):
        self.co = cohere.Client(os.getenv("COHERE_API_KEY"))
        self.model = "command-r"  # Using Cohere's Command-R model as specified in requirements

    def generate_response_full_rag(self, query: str, context_documents: List[Dict[str, Any]]) -> str:
        """
        Generate response using full-book RAG mode with retrieved documents as context
        """
        if not context_documents:
            # Handle case where no documents were retrieved
            prompt = f"""
            You are an expert assistant for the Humanoid Robotics textbook.
            I couldn't find specific information about your question in the textbook content.

            Question: {query}

            Please acknowledge that you don't have specific information from the textbook about this topic,
            but if you have general knowledge about humanoid robotics that could be helpful,
            you may provide that information while clearly stating it's general knowledge
            and not from the specific textbook content.
            """
        else:
            # Format the context from retrieved documents
            context = "\n\n".join([doc["text"] for doc in context_documents])

            prompt = f"""
            You are an expert assistant for the Humanoid Robotics textbook.
            Answer the user's question based on the provided context from the book.

            Context: {context}

            Question: {query}

            Please provide a comprehensive answer based on the context, citing the relevant sources.
            If the answer cannot be found in the provided context, politely inform the user.
            """

        try:
            response = self.co.generate(
                model=self.model,
                prompt=prompt,
                max_tokens=500,
                temperature=0.3  # Low temperature for factual accuracy
            )

            return response.generations[0].text.strip()
        except Exception as e:
            print(f"Error generating response with Cohere: {e}")
            return "I encountered an error while processing your request. Please try again."

    def generate_response_selected_text(self, query: str, selected_text: str) -> str:
        """
        Generate response using selected-text-only mode, strictly using only the provided text
        """
        prompt = f"""
        You are an expert assistant for the Humanoid Robotics textbook.
        Answer the user's question based ONLY on the selected text provided below.
        Do not use any external knowledge or information beyond what's in the selected text.

        Selected Text: {selected_text}

        Question: {query}

        Please provide an answer based only on the selected text.
        """

        try:
            response = self.co.generate(
                model=self.model,
                prompt=prompt,
                max_tokens=500,
                temperature=0.3  # Low temperature for factual accuracy
            )

            return response.generations[0].text.strip()
        except Exception as e:
            print(f"Error generating response with Cohere: {e}")
            return "I encountered an error while processing your request. Please try again."