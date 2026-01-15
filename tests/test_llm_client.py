"""
Tests for markpdfdown.core.llm_client module
"""

import base64
import os
from unittest.mock import MagicMock, patch

import pytest

from markpdfdown.core.llm_client import LLMClient


class TestLLMClientInit:
    """Tests for LLMClient initialization"""

    def test_init_with_model_name(self):
        """Test LLMClient initialization with model name"""
        client = LLMClient("gpt-4o")
        assert client.model_name == "gpt-4o"

    def test_init_with_openrouter_model(self):
        """Test LLMClient initialization with OpenRouter model"""
        client = LLMClient("openrouter/anthropic/claude-3.5-sonnet")
        assert client.model_name == "openrouter/anthropic/claude-3.5-sonnet"


class TestLLMClientCompletion:
    """Tests for LLMClient.completion method"""

    def test_completion_basic(self, mock_litellm_completion, mock_llm_response):
        """Test basic completion call"""
        client = LLMClient("gpt-4o")
        result = client.completion("Hello, world!")

        assert result == mock_llm_response
        mock_litellm_completion.assert_called_once()

    def test_completion_with_system_prompt(self, mock_litellm_completion):
        """Test completion with system prompt"""
        client = LLMClient("gpt-4o")
        client.completion("Hello", system_prompt="You are helpful")

        call_args = mock_litellm_completion.call_args
        messages = call_args.kwargs["messages"]

        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[0]["content"] == "You are helpful"
        assert messages[1]["role"] == "user"

    def test_completion_with_image(self, mock_litellm_completion, sample_image_path):
        """Test completion with image input"""
        client = LLMClient("gpt-4o")
        client.completion("Describe this image", image_paths=[sample_image_path])

        call_args = mock_litellm_completion.call_args
        messages = call_args.kwargs["messages"]
        user_content = messages[0]["content"]

        # Should have text and image
        assert len(user_content) == 2
        assert user_content[0]["type"] == "text"
        assert user_content[1]["type"] == "image_url"
        assert "base64" in user_content[1]["image_url"]["url"]

    def test_completion_with_multiple_images(self, mock_litellm_completion, images_dir):
        """Test completion with multiple images"""
        image_paths = [
            os.path.join(images_dir, "demo_01.png"),
            os.path.join(images_dir, "demo_02.png"),
        ]

        client = LLMClient("gpt-4o")
        client.completion("Describe these images", image_paths=image_paths)

        call_args = mock_litellm_completion.call_args
        messages = call_args.kwargs["messages"]
        user_content = messages[0]["content"]

        # Should have text and 2 images
        assert len(user_content) == 3
        assert user_content[0]["type"] == "text"
        assert user_content[1]["type"] == "image_url"
        assert user_content[2]["type"] == "image_url"

    def test_completion_with_custom_params(self, mock_litellm_completion):
        """Test completion with custom parameters"""
        client = LLMClient("gpt-4o")
        client.completion(
            "Hello",
            temperature=0.7,
            max_tokens=1024,
        )

        call_args = mock_litellm_completion.call_args
        assert call_args.kwargs["temperature"] == 0.7
        assert call_args.kwargs["max_tokens"] == 1024

    def test_completion_retry_on_failure(self):
        """Test completion retries on failure"""
        with patch("markpdfdown.core.llm_client.completion") as mock_completion:
            # First two calls fail, third succeeds
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Success"

            mock_completion.side_effect = [
                Exception("API Error"),
                Exception("API Error"),
                mock_response,
            ]

            client = LLMClient("gpt-4o")
            with patch("markpdfdown.core.llm_client.time.sleep"):
                result = client.completion("Hello", retry_times=3)

            assert result == "Success"
            assert mock_completion.call_count == 3

    def test_completion_raises_after_max_retries(self):
        """Test completion raises exception after max retries"""
        with patch("markpdfdown.core.llm_client.completion") as mock_completion:
            mock_completion.side_effect = Exception("API Error")

            client = LLMClient("gpt-4o")
            with patch("markpdfdown.core.llm_client.time.sleep"):
                with pytest.raises(Exception, match="API Error"):
                    client.completion("Hello", retry_times=3)

            assert mock_completion.call_count == 3

    def test_completion_no_choices_raises(self):
        """Test completion raises when no choices returned"""
        with patch("markpdfdown.core.llm_client.completion") as mock_completion:
            mock_response = MagicMock()
            mock_response.choices = []
            mock_completion.return_value = mock_response

            client = LLMClient("gpt-4o")
            with patch("markpdfdown.core.llm_client.time.sleep"):
                with pytest.raises(Exception, match="No response from API"):
                    client.completion("Hello", retry_times=1)


class TestLLMClientEncodeImage:
    """Tests for LLMClient._encode_image method"""

    def test_encode_image(self, sample_image_path):
        """Test image encoding to base64"""
        client = LLMClient("gpt-4o")
        result = client._encode_image(sample_image_path)

        # Verify it's valid base64
        decoded = base64.b64decode(result)
        assert len(decoded) > 0

        # Verify PNG magic bytes
        assert decoded[:4] == b"\x89PNG"

    def test_encode_image_returns_string(self, sample_image_path):
        """Test encode_image returns string"""
        client = LLMClient("gpt-4o")
        result = client._encode_image(sample_image_path)
        assert isinstance(result, str)

    def test_encode_nonexistent_file_raises(self):
        """Test encoding nonexistent file raises error"""
        client = LLMClient("gpt-4o")
        with pytest.raises(FileNotFoundError):
            client._encode_image("/nonexistent/image.png")
