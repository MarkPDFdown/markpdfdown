"""
Utility functions for MarkPDFDown
"""

import re
from typing import Optional


def remove_markdown_wrap(text: str, language: str = "markdown") -> str:
    """
    Remove markdown code block wrapper from text

    Args:
        text: Input text that may be wrapped in markdown code blocks
        language: Expected language identifier in code block

    Returns:
        Text with markdown wrapper removed
    """
    if not text:
        return text

    # Pattern to match markdown code blocks
    pattern = rf"```{re.escape(language)}\s*\n?(.*?)\n?```"

    # Try to find and extract content from code block
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # If no code block found, return original text
    return text.strip()


def detect_file_type(file_data: bytes) -> Optional[str]:
    """
    Detect file type from binary data

    Args:
        file_data: Binary file data

    Returns:
        File extension (with dot) or None if not recognized
    """
    if not file_data:
        return None

    # PDF file magic number
    if file_data.startswith(b"%PDF-"):
        return ".pdf"

    # JPEG file magic numbers
    elif file_data.startswith(b"\xff\xd8\xff\xdb") or file_data.startswith(
        b"\xff\xd8\xff\xe0"
    ):
        return ".jpg"

    # PNG file magic number
    elif file_data.startswith(b"\x89\x50\x4e\x47"):
        return ".png"

    # BMP file magic number
    elif file_data.startswith(b"\x42\x4d"):
        return ".bmp"

    # GIF file magic number
    elif file_data.startswith(b"GIF87a") or file_data.startswith(b"GIF89a"):
        return ".gif"

    return None


def validate_page_range(
    start_page: int, end_page: int, total_pages: int
) -> tuple[int, int]:
    """
    Validate and normalize page range

    Args:
        start_page: Starting page number (1-based)
        end_page: Ending page number (1-based, 0 means last page)
        total_pages: Total number of pages in document

    Returns:
        Tuple of (normalized_start, normalized_end)

    Raises:
        ValueError: If page range is invalid
    """
    if start_page < 1:
        raise ValueError("Start page must be >= 1")

    if start_page > total_pages:
        raise ValueError(f"Start page {start_page} exceeds total pages {total_pages}")

    # Handle end_page = 0 (means last page)
    if end_page == 0:
        end_page = total_pages

    if end_page < start_page:
        raise ValueError(f"End page {end_page} must be >= start page {start_page}")

    if end_page > total_pages:
        end_page = total_pages

    return start_page, end_page
