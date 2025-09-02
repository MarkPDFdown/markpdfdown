import logging
from typing import Optional

import openai

logger = logging.getLogger(__name__)


class LLMClient:
    """
    OpenAI API compatible client class
    """

    def __init__(self, base_url: str, api_key: str, model: str):
        """
        Initialize OpenAI API client
        :param base_url: Base URL for OpenAI API
        :param api_key: OpenAI API key
        :param model: Name of the model to use
        """
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        self.client = openai.OpenAI(base_url=base_url, api_key=api_key)

    def completion(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        image_paths: Optional[list[str]] = None,
        temperature: float = 0.7,
        max_tokens: int = 8192,
        reasoning_effort: Optional[str] = None,
    ) -> str:
        """
        Create chat dialogue (supports multimodal)

        Args:
            user_message: User message content
            system_prompt: System prompt (optional)
            image_paths: List of image paths (optional)
            temperature: Generation temperature
            max_tokens: Maximum number of tokens

        Returns:
            str: Model generated response content
        """
        # Create the message content
        user_content = [{"type": "text", "text": user_message}]
        if image_paths:
            for img_path in image_paths:
                base64_image = self.encode_image(img_path)
                user_content.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    }
                )

        messages = []
        if system_prompt:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ]
        else:
            messages = [{"role": "user", "content": user_content}]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                reasoning_effort=reasoning_effort,
                extra_headers={
                    "X-Title": "MarkPDFdown",
                    "HTTP-Referer": "https://github.com/MarkPDFdown/markpdfdown.git",
                },
            )
            if not response.choices:
                raise Exception("No response from API")
            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"API request failed: {str(e)}")
            raise e

    def encode_image(self, image_path: str) -> str:
        import base64

        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
