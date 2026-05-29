

import json
import re
import logging
from typing import Optional, Dict, Any, List
from openai import OpenAI

from ..config import Config

logger = logging.getLogger(__name__)


class LLMClient:
    
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.api_key = api_key or Config.LLM_API_KEY
        self.base_url = base_url or Config.LLM_BASE_URL
        self.model = model or Config.LLM_MODEL_NAME
        
        if not self.api_key:
            raise ValueError("LLM_API_KEY is not configured")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[Dict] = None
    ) -> str:
        
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        if response_format:
            kwargs["response_format"] = response_format

        logger.info(
            "Calling LLM: model=%s, base_url=%s, response_format=%s",
            self.model,
            self.base_url,
            response_format
        )
        
        response = self.client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content or ""
        
        content = re.sub(r'<think>[\s\S]*?</think>', '', content).strip()

        logger.info("LLM response length: %s", len(content))
        if not content:
            logger.warning("LLM returned empty content, finish_reason=%s", getattr(response.choices[0], "finish_reason", None))

        return content
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        
        cleaned_response = (response or "").strip()
        cleaned_response = re.sub(
            r'^```(?:json)?\s*\n?', '', cleaned_response, flags=re.IGNORECASE
        )
        cleaned_response = re.sub(r'\n?```\s*$', '', cleaned_response)
        cleaned_response = cleaned_response.strip()

        if not cleaned_response:
            raise ValueError("LLM returned empty content")

        try:
            data = json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON. First 500 characters of raw response: %s", cleaned_response[:500])
            raise ValueError(f"LLM returned invalid JSON: {cleaned_response}") from e

        if not isinstance(data, dict):
            raise ValueError(f"LLM returned JSON that is not an object: {cleaned_response}")

        return data
    
    def chat_json(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        
        
        try:
            response = self.chat(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"}
            )
            return self._parse_json_response(response)
        except Exception as e:
            logger.exception("JSON mode call failed, falling back to plain text mode: %s", e)

        
        fallback_messages = messages + [
            {
                "role": "system",
                "content": "Return only a valid JSON object. Do not include markdown code fences or explanations."
            }
        ]

        try:
            response = self.chat(
                messages=fallback_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format=None
            )
            return self._parse_json_response(response)
        except Exception as e:
            logger.exception("Plain text fallback mode also failed: %s", e)
            raise
