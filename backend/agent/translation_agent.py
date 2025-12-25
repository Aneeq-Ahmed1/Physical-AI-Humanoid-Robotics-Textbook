from typing import Dict, Any
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class TranslationAgent:
    """
    Agent responsible for translating text between English and Urdu
    """
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required for translation")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def translate_text(self, text: str, target_language: str, source_language: str = "en") -> str:
        """
        Translate text from source language to target language

        Args:
            text: Text to translate
            target_language: Target language code ('ur' for Urdu, 'en' for English)
            source_language: Source language code ('en' for English, 'ur' for Urdu)

        Returns:
            Translated text
        """
        if source_language == target_language:
            return text

        # Create appropriate prompt based on translation direction
        if source_language == "en" and target_language == "ur":
            prompt = f"""
            Translate the following English text to Urdu.
            Preserve the meaning and context accurately.

            Text to translate:
            {text}

            Translation in Urdu:
            """
        elif source_language == "ur" and target_language == "en":
            prompt = f"""
            Translate the following Urdu text to English.
            Preserve the meaning and context accurately.

            Text to translate:
            {text}

            Translation in English:
            """
        else:
            raise ValueError(f"Unsupported translation from {source_language} to {target_language}")

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    max_output_tokens=2000,  # Allow for longer translations
                    temperature=0.1,  # Low temperature for accuracy
                ),
                safety_settings={
                    "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                    "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                    "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                    "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
                }
            )

            if response.text:
                return response.text.strip()
            else:
                raise Exception("No translation returned from Gemini")

        except Exception as e:
            print(f"Translation error: {str(e)}")
            raise Exception(f"Translation failed: {str(e)}")

    def translate_query(self, query: str, target_language: str) -> str:
        """
        Translate a query to the target language
        """
        return self.translate_text(query, target_language, "en")

    def translate_response(self, response: str, source_language: str) -> str:
        """
        Translate a response from the source language to English for user
        """
        return self.translate_text(response, "en", source_language)

    def translate_documents(self, documents: list, target_language: str, source_language: str = "en") -> list:
        """
        Translate a list of documents to the target language
        Each document is expected to have a 'text' field
        """
        translated_docs = []
        for doc in documents:
            translated_doc = doc.copy()  # Copy all fields
            if 'text' in doc:
                translated_doc['text'] = self.translate_text(doc['text'], target_language, source_language)
            translated_docs.append(translated_doc)

        return translated_docs