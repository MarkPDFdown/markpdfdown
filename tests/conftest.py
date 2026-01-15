"""
Pytest configuration and shared fixtures for markpdfdown tests
"""

import os
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def fixtures_dir():
    """Return the fixtures directory path"""
    return os.path.join(os.path.dirname(__file__), "fixtures")


@pytest.fixture
def images_dir(fixtures_dir):
    """Return the images directory path"""
    return os.path.join(fixtures_dir, "images")


@pytest.fixture
def pdfs_dir(fixtures_dir):
    """Return the pdfs directory path"""
    return os.path.join(fixtures_dir, "pdfs")


@pytest.fixture
def expected_dir(fixtures_dir):
    """Return the expected outputs directory path"""
    return os.path.join(fixtures_dir, "expected")


@pytest.fixture
def sample_image_path(images_dir):
    """Return a sample image path for testing"""
    return os.path.join(images_dir, "demo_01.png")


@pytest.fixture
def sample_pdf_path(pdfs_dir):
    """Return a sample PDF path for testing"""
    return os.path.join(pdfs_dir, "input_tables.pdf")


@pytest.fixture
def mock_llm_response():
    """Return a mock LLM response content"""
    return "# Sample Markdown\n\nThis is a test response."


@pytest.fixture
def mock_litellm_completion(mock_llm_response):
    """Mock litellm.completion for testing LLMClient"""
    with patch("markpdfdown.core.llm_client.completion") as mock_completion:
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = mock_llm_response
        mock_completion.return_value = mock_response
        yield mock_completion


@pytest.fixture
def sample_png_bytes():
    """Return sample PNG file bytes (magic number)"""
    return b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a" + b"\x00" * 100


@pytest.fixture
def sample_pdf_bytes():
    """Return sample PDF file bytes (magic number)"""
    return b"%PDF-1.4\n" + b"\x00" * 100


@pytest.fixture
def sample_jpg_bytes():
    """Return sample JPEG file bytes (magic number)"""
    return b"\xff\xd8\xff\xe0" + b"\x00" * 100
