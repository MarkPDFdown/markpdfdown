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
    Unified LLM client using LiteLLM
    Supports OpenAI and OpenRouter automatically
    """

    def __init__(self, model_name: str):
        """
        Initialize LLM client

        Args:
            model_name: Model name (e.g., "gpt-4o", "openrouter/anthropic/claude-3.5-sonnet")
        """
        self.model_name = model_name

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

        # Retry mechanism
        for attempt in range(retry_times):
            try:
                response = completion(
                    model=self.model_name,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    # Add custom headers for tracking
                    extra_headers={
                        "X-Title": "MarkPDFdown",
                        "HTTP-Referer": "https://github.com/MarkPDFdown/markpdfdown.git",
                    },
                )

                if not response.choices:
                    raise Exception("No response from API")

                return response.choices[0].message.content

            except Exception as e:
                logger.error(
                    f"API request failed (attempt {attempt + 1}/{retry_times}): {str(e)}"
                )
                if attempt < retry_times - 1:
                    # Wait before retry
                    time.sleep(0.5 * (attempt + 1))
                else:
                    raise e

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
