"""
Tests for markpdfdown.core.utils module
"""

import pytest

from markpdfdown.core.utils import (
    detect_file_type,
    remove_markdown_wrap,
    validate_page_range,
)


class TestRemoveMarkdownWrap:
    """Tests for remove_markdown_wrap function"""

    def test_remove_markdown_wrapper(self):
        """Test removing markdown code block wrapper"""
        text = "```markdown\n# Hello World\n```"
        result = remove_markdown_wrap(text)
        assert result == "# Hello World"

    def test_remove_markdown_wrapper_with_newlines(self):
        """Test removing wrapper with multiple newlines"""
        text = "```markdown\n\n# Hello\n\nContent here\n\n```"
        result = remove_markdown_wrap(text)
        assert result == "# Hello\n\nContent here"

    def test_no_wrapper_returns_stripped(self):
        """Test text without wrapper returns stripped text"""
        text = "  # Hello World  "
        result = remove_markdown_wrap(text)
        assert result == "# Hello World"

    def test_empty_text_returns_empty(self):
        """Test empty text returns empty"""
        assert remove_markdown_wrap("") == ""
        assert remove_markdown_wrap(None) is None

    def test_different_language_tag(self):
        """Test with different language tag"""
        text = "```python\nprint('hello')\n```"
        result = remove_markdown_wrap(text, language="python")
        assert result == "print('hello')"

    def test_case_insensitive_language(self):
        """Test language matching is case insensitive"""
        text = "```MARKDOWN\n# Title\n```"
        result = remove_markdown_wrap(text, language="markdown")
        assert result == "# Title"

    def test_nested_code_blocks(self):
        """Test with nested code blocks"""
        text = "```markdown\nSome text\n```python\ncode\n```\nMore text\n```"
        result = remove_markdown_wrap(text)
        # Should extract the outer markdown block content
        assert "Some text" in result


class TestDetectFileType:
    """Tests for detect_file_type function"""

    def test_detect_pdf(self):
        """Test PDF detection"""
        pdf_data = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3"
        assert detect_file_type(pdf_data) == ".pdf"

    def test_detect_png(self, sample_png_bytes):
        """Test PNG detection"""
        assert detect_file_type(sample_png_bytes) == ".png"

    def test_detect_jpeg_e0(self, sample_jpg_bytes):
        """Test JPEG detection (FFD8FFE0)"""
        assert detect_file_type(sample_jpg_bytes) == ".jpg"

    def test_detect_jpeg_db(self):
        """Test JPEG detection (FFD8FFDB)"""
        jpg_data = b"\xff\xd8\xff\xdb" + b"\x00" * 100
        assert detect_file_type(jpg_data) == ".jpg"

    def test_detect_bmp(self):
        """Test BMP detection"""
        bmp_data = b"\x42\x4d" + b"\x00" * 100
        assert detect_file_type(bmp_data) == ".bmp"

    def test_detect_gif87a(self):
        """Test GIF87a detection"""
        gif_data = b"GIF87a" + b"\x00" * 100
        assert detect_file_type(gif_data) == ".gif"

    def test_detect_gif89a(self):
        """Test GIF89a detection"""
        gif_data = b"GIF89a" + b"\x00" * 100
        assert detect_file_type(gif_data) == ".gif"

    def test_empty_data_returns_none(self):
        """Test empty data returns None"""
        assert detect_file_type(b"") is None
        assert detect_file_type(None) is None

    def test_unknown_type_returns_none(self):
        """Test unknown file type returns None"""
        unknown_data = b"\x00\x01\x02\x03\x04\x05"
        assert detect_file_type(unknown_data) is None


class TestValidatePageRange:
    """Tests for validate_page_range function"""

    def test_valid_range(self):
        """Test valid page range"""
        start, end = validate_page_range(1, 5, 10)
        assert start == 1
        assert end == 5

    def test_end_zero_means_last_page(self):
        """Test end_page=0 means last page"""
        start, end = validate_page_range(1, 0, 10)
        assert start == 1
        assert end == 10

    def test_single_page(self):
        """Test single page range"""
        start, end = validate_page_range(5, 5, 10)
        assert start == 5
        assert end == 5

    def test_end_exceeds_total_clamped(self):
        """Test end page exceeding total is clamped"""
        start, end = validate_page_range(1, 20, 10)
        assert start == 1
        assert end == 10

    def test_start_page_less_than_one_raises(self):
        """Test start page < 1 raises ValueError"""
        with pytest.raises(ValueError, match="Start page must be >= 1"):
            validate_page_range(0, 5, 10)

    def test_start_exceeds_total_raises(self):
        """Test start page exceeding total raises ValueError"""
        with pytest.raises(ValueError, match="exceeds total pages"):
            validate_page_range(15, 20, 10)

    def test_end_less_than_start_raises(self):
        """Test end page < start page raises ValueError"""
        with pytest.raises(ValueError, match="must be >= start page"):
            validate_page_range(5, 3, 10)

    def test_full_document(self):
        """Test full document range"""
        start, end = validate_page_range(1, 10, 10)
        assert start == 1
        assert end == 10

    def test_last_page_only(self):
        """Test last page only"""
        start, end = validate_page_range(10, 10, 10)
        assert start == 10
        assert end == 10
