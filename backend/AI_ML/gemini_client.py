import os
from typing import Any, Optional

from google import genai
from google.genai import types as genai_types


class GeminiClient:
    """Compatibility wrapper around the modern Google GenAI SDK."""

    supported_models = [
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
    ]

    def __init__(self, api_key: Optional[str] = None):
        key = api_key or os.getenv("GEMINI_API_KEY")
        self.api_key = key
        if key:
            self.client = genai.Client(api_key=key)
        else:
            self.client = None

    def generate_text(
        self,
        prompt: str,
        model_name: Optional[str] = None,
        temperature: float = 0.2,
        max_output_tokens: int = 8000,
    ) -> str:
        if not self.client:
            raise ValueError("No API key provided for GeminiClient")

        target_model = (model_name or self.supported_models[0]).strip()
        response = self.client.models.generate_content(
            model=target_model,
            contents=prompt,
            config=genai_types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_output_tokens,
            ),
        )
        return self._extract_text(response)

    @staticmethod
    def _extract_text(response: Any) -> str:
        if hasattr(response, "text") and response.text:
            return response.text

        candidates = getattr(response, "candidates", None) or []
        if candidates:
            first = candidates[0]
            content = getattr(first, "content", None)
            parts = getattr(content, "parts", None) or []
            extracted = []
            for part in parts:
                if hasattr(part, "text") and part.text:
                    extracted.append(part.text)
            if extracted:
                return "".join(extracted)

        return str(response)
