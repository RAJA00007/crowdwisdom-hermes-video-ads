"""Hermes LLM Client using OpenRouter / OpenAI API interface.

Provides connection diagnostics, structured generation, and fallback handling.
Compatible with Python 3.10.
"""

import json
from typing import Any, Dict, List, Optional
from openai import OpenAI, APIError, AuthenticationError
from config.settings import get_settings


class HermesLLMClient:
    """Client for invoking Nous Research Hermes models via OpenRouter or OpenAI-compatible endpoint."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
    ):
        settings = get_settings()
        self.api_key = api_key or settings.openrouter_api_key
        self.base_url = base_url or settings.openrouter_base_url
        self.model = model or settings.hermes_model
        self.temperature = settings.llm_temperature
        self.max_tokens = settings.llm_max_tokens

        if not self.api_key or self.api_key == "your_openrouter_api_key_here":
            self.client = None
        else:
            self.client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key,
                timeout=60.0,
                default_headers={
                    "HTTP-Referer": "https://github.com/crowdwisdom/video-ads-agent",
                    "X-Title": "CrowdWisdom Video Ads Agent",
                },
            )

    def is_configured(self) -> bool:
        """Check if client has a valid API key configured."""
        return bool(self.client and self.api_key and self.api_key != "your_openrouter_api_key_here")

    def test_connection(self) -> Dict[str, Any]:
        """Test connectivity to OpenRouter / Hermes model."""
        if not self.is_configured():
            return {
                "success": False,
                "error": "OPENROUTER_API_KEY is not configured in .env",
                "model": self.model,
                "endpoint": self.base_url,
            }

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are Hermes, an expert multi-agent orchestrator.",
                    },
                    {
                        "role": "user",
                        "content": "Respond with the single word: READY",
                    },
                ],
                max_tokens=20,
                temperature=0.0,
            )
            reply = response.choices[0].message.content.strip()
            return {
                "success": True,
                "model": self.model,
                "endpoint": self.base_url,
                "response": reply,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                },
            }
        except AuthenticationError as e:
            return {
                "success": False,
                "error": f"Authentication failed: {str(e)}",
                "model": self.model,
                "endpoint": self.base_url,
            }
        except APIError as e:
            return {
                "success": False,
                "error": f"API Error: {str(e)}",
                "model": self.model,
                "endpoint": self.base_url,
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "model": self.model,
                "endpoint": self.base_url,
            }

    def generate_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        response_format: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Generate a chat completion from Hermes."""
        if not self.is_configured():
            raise ValueError("OpenRouter API key is not configured. Please set OPENROUTER_API_KEY in .env")

        kwargs: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature if temperature is not None else self.temperature,
            "max_tokens": max_tokens if max_tokens is not None else self.max_tokens,
        }

        if response_format:
            kwargs["response_format"] = response_format

        response = self.client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content
        return {
            "content": content,
            "finish_reason": response.choices[0].finish_reason,
            "model": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                "completion_tokens": response.usage.completion_tokens if response.usage else 0,
            },
        }

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
    ) -> Dict[str, Any]:
        """Generate and parse structured JSON output."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        result = self.generate_completion(
            messages=messages,
            temperature=temperature,
            response_format={"type": "json_object"},
        )
        content = result["content"]
        try:
            parsed = json.loads(content)
            return {"success": True, "data": parsed, "raw": content}
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"JSON decode error: {str(e)}",
                "raw": content,
            }
