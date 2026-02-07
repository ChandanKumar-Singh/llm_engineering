from typing import Any, Dict, List, Optional, Type
from openai import OpenAI
from pydantic import BaseModel
from ..config import config

class LLMService:
    """Wrapper around OpenAI API for easy agent usage."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.client = OpenAI(api_key=api_key or (config.openai_api_key if config else None))
        self.model = model or (config.model_name if config else "gpt-4o")

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        response_format: Optional[Type[BaseModel]] = None
    ) -> Any:
        """
        Send a chat completion request to the LLM.
        
        Args:
            messages: List of message dictionaries.
            tools: Optional list of tool definitions.
            response_format: Optional Pydantic model for structured output validation.
        """
        params = {
            "model": self.model,
            "messages": messages,
        }

        if tools:
            params["tools"] = tools
            params["tool_choice"] = "auto"

        if response_format:
            # support new structured output if available, or simplified parsing
            # For this 'canonical' example, we'll try the beta parse if pydantic model provided
            try:
                completion = self.client.beta.chat.completions.parse(
                    **params,
                    response_format=response_format
                )
                return completion.choices[0].message
            except Exception as e:
                # Fallback or re-raise
                print(f"Error in structured parsing: {e}")
                raise e
        else:
            completion = self.client.chat.completions.create(**params)
            return completion.choices[0].message
