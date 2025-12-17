import google.generativeai as genai
from typing import List, Dict, Any, Union
import time


class MockChatCompletionMessage:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content


class MockChoice:
    def __init__(self, index: int, message, finish_reason: str):
        self.index = index
        self.message = message
        self.finish_reason = finish_reason


class MockUsage:
    def __init__(self, prompt_tokens: int, completion_tokens: int, total_tokens: int):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.total_tokens = total_tokens


class MockChatCompletion:
    def __init__(self, id: str, choices: List, created: int, model: str, object: str, usage):
        self.id = id
        self.choices = choices
        self.created = created
        self.model = model
        self.object = object
        self.usage = usage


class GeminiChatCompletions:
    def __init__(self, model):
        self.model = model

    def create(
        self,
        model: str,
        messages: List[Dict[str, str]],
        max_tokens: int = 500,
        temperature: float = 0.3,
        **kwargs
    ):
        # Convert messages to a single prompt
        prompt_parts = []
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            if role == "system":
                # System messages are handled as part of the first user message or context
                prompt_parts.append(f"{content}\n\n")
            elif role == "user":
                prompt_parts.append(content)
            elif role == "assistant":
                # For Gemini, we'll format assistant messages as part of the context
                prompt_parts.append(f"Assistant response: {content}\n\n")

        full_prompt = "".join(prompt_parts)

        # Generate content using Gemini
        try:
            # Configure safety settings to be more permissive for educational content
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature
                ),
                safety_settings={
                    "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                    "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                    "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                    "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
                }
            )

            # Create a mock OpenAI-like response
            if response.text:
                message = MockChatCompletionMessage(
                    role="assistant",
                    content=response.text.strip(),
                )

                choice = MockChoice(
                    index=0,
                    message=message,
                    finish_reason="stop"
                )

                # Create mock usage data (approximate)
                prompt_tokens = len(full_prompt.split())
                completion_tokens = len(response.text.split()) if response.text else 0
                total_tokens = prompt_tokens + completion_tokens

                usage = MockUsage(
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=total_tokens
                )

                return MockChatCompletion(
                    id=f"chatcmpl-{int(time.time())}",
                    choices=[choice],
                    created=int(time.time()),
                    model=model,
                    object="chat.completion",
                    usage=usage
                )
            else:
                raise Exception("No response text from Gemini")
        except Exception as e:
            # Re-raise with more context for debugging
            raise Exception(f"Gemini API error: {str(e)}")


class OpenAIGeminiClient:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self._gemini_model = genai.GenerativeModel('gemini-2.5-flash')  # Use available latest model
        self.chat = type('Chat', (), {
            'completions': GeminiChatCompletions(self._gemini_model)
        })()