"""
LLM client using LiteLLM for unified API access
"""

import base64
import logging
import time
from typing import Optional

import litellm
from litellm import completion

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Unified LLM client using LiteLLM.
    Supports OpenAI, OpenRouter, Anthropic, Gemini, Ollama, etc.
    Supports fallback models when rate limits or errors occur.
    """

    def __init__(
        self,
        model_name: str,
        fallback_models: Optional[list[str]] = None,
    ):
        """
        Initialize LLM client.

        Args:
            model_name: Primary model name (e.g., "gpt-4o")
            fallback_models: Optional list of fallback model names to try if primary fails
        """
        self.model_name = model_name
        self.fallback_models = fallback_models or []
        self.active_model = model_name
        # Configure LiteLLM logging
        litellm.set_verbose = False

    def completion(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        image_paths: Optional[list[str]] = None,
        temperature: float = 0.3,
        max_tokens: int = 8192,
        retry_times: int = 3,
    ) -> str:
        """
        Create chat completion with multimodal support

        Args:
            user_message: User message content
            system_prompt: System prompt (optional)
            image_paths: List of image paths (optional)
            temperature: Generation temperature
            max_tokens: Maximum number of tokens
            retry_times: Number of retries

        Returns:
            Generated response content
        """
        # Build user content with text and images
        user_content = [{"type": "text", "text": user_message}]

        if image_paths:
            for img_path in image_paths:
                base64_image = self._encode_image(img_path)
                user_content.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    }
                )

        # Build messages
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_content})

        # Candidate model chain: active model first, then remaining fallback models
        models_to_try = [self.active_model] + [
            m for m in self.fallback_models if m != self.active_model
        ]

        last_exception: Optional[Exception] = None

        for model in models_to_try:
            for attempt in range(retry_times):
                try:
                    response = completion(
                        model=model,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        extra_headers={
                            "X-Title": "MarkPDFdown",
                            "HTTP-Referer": "https://github.com/MarkPDFdown/markpdfdown.git",
                        },
                    )

                    if not response.choices:
                        raise Exception(f"No response from API for model {model}")

                    # Switch active model to this working model for future calls
                    if self.active_model != model:
                        logger.info(
                            f"Switched active model from {self.active_model} to fallback model: {model}"
                        )
                        self.active_model = model

                    return response.choices[0].message.content

                except Exception as e:
                    last_exception = e
                    logger.warning(
                        f"API request failed on model '{model}' (attempt {attempt + 1}/{retry_times}): {e}"
                    )
                    if attempt < retry_times - 1:
                        time.sleep(0.5 * (attempt + 1))

            logger.warning(f"All {retry_times} retries failed for model '{model}'.")
            if model != models_to_try[-1]:
                logger.info(f"Falling back from '{model}' to next candidate model...")

        if last_exception:
            raise last_exception

        return ""

    def _encode_image(self, image_path: str) -> str:
        """
        Encode image to base64 string

        Args:
            image_path: Path to image file

        Returns:
            Base64 encoded image string
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
