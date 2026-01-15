"""
Tests for markpdfdown.main module
"""

import os
from unittest.mock import MagicMock, patch

import pytest

from markpdfdown.main import (
    convert_from_file,
    convert_from_stdin,
    convert_image_to_markdown,
    convert_to_markdown,
)


class TestConvertImageToMarkdown:
    """Tests for convert_image_to_markdown function"""

    def test_convert_image_success(self, sample_image_path, mock_llm_response):
        """Test successful image to markdown conversion"""
        mock_client = MagicMock()
        mock_client.completion.return_value = "```markdown\n# Title\n```"

        result = convert_image_to_markdown(sample_image_path, mock_client)

        assert result == "# Title"
        mock_client.completion.assert_called_once()

    def test_convert_image_uses_image_path(self, sample_image_path):
        """Test image path is passed to LLM client"""
        mock_client = MagicMock()
        mock_client.completion.return_value = "# Content"

        convert_image_to_markdown(sample_image_path, mock_client)

        call_kwargs = mock_client.completion.call_args.kwargs
        assert call_kwargs["image_paths"] == [sample_image_path]

    def test_convert_image_failure_returns_empty(self, sample_image_path):
        """Test conversion failure returns empty string"""
        mock_client = MagicMock()
        mock_client.completion.side_effect = Exception("API Error")

        result = convert_image_to_markdown(sample_image_path, mock_client)

        assert result == ""

    def test_convert_image_removes_markdown_wrap(self, sample_image_path):
        """Test markdown wrapper is removed from response"""
        mock_client = MagicMock()
        mock_client.completion.return_value = "```markdown\n# Hello World\n```"

        result = convert_image_to_markdown(sample_image_path, mock_client)

        assert result == "# Hello World"
        assert "```" not in result


class TestConvertToMarkdown:
    """Tests for convert_to_markdown function"""

    def test_empty_input_raises(self):
        """Test empty input raises ValueError"""
        with pytest.raises(ValueError, match="No input data provided"):
            convert_to_markdown(b"")

    def test_unsupported_file_type_raises(self):
        """Test unsupported file type raises ValueError"""
        with pytest.raises(ValueError, match="Unsupported file type"):
            convert_to_markdown(b"unknown file content", cleanup=False)

    @patch("markpdfdown.main.LLMClient")
    @patch("markpdfdown.main.create_worker")
    def test_convert_png_image(self, mock_create_worker, mock_llm_class, tmp_path):
        """Test converting PNG image"""
        # Setup mock worker
        mock_worker = MagicMock()
        mock_worker.convert_to_images.return_value = [str(tmp_path / "image.png")]
        mock_create_worker.return_value = mock_worker

        # Setup mock LLM client
        mock_llm = MagicMock()
        mock_llm.completion.return_value = "# Converted Content"
        mock_llm_class.return_value = mock_llm

        # Create fake image file
        (tmp_path / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)

        # Run conversion
        png_data = b"\x89\x50\x4e\x47" + b"\x00" * 100
        result = convert_to_markdown(
            png_data,
            output_dir=str(tmp_path),
            cleanup=False,
        )

        assert "# Converted Content" in result
        mock_create_worker.assert_called_once()

    @patch("markpdfdown.main.LLMClient")
    @patch("markpdfdown.main.create_worker")
    def test_convert_with_filename_extension(
        self, mock_create_worker, mock_llm_class, tmp_path
    ):
        """Test conversion uses filename extension"""
        mock_worker = MagicMock()
        mock_worker.convert_to_images.return_value = [str(tmp_path / "image.png")]
        mock_create_worker.return_value = mock_worker

        mock_llm = MagicMock()
        mock_llm.completion.return_value = "# Content"
        mock_llm_class.return_value = mock_llm

        (tmp_path / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)

        convert_to_markdown(
            b"some data",
            input_filename="test.png",
            output_dir=str(tmp_path),
            cleanup=False,
        )

        # Should have created worker with .png extension
        call_args = mock_create_worker.call_args
        assert call_args[0][0].endswith(".png")

    @patch("markpdfdown.main.LLMClient")
    @patch("markpdfdown.main.create_worker")
    def test_convert_multiple_pages(self, mock_create_worker, mock_llm_class, tmp_path):
        """Test conversion of multiple pages"""
        # Create fake images
        (tmp_path / "page_001.png").write_bytes(b"\x89PNG" + b"\x00" * 100)
        (tmp_path / "page_002.png").write_bytes(b"\x89PNG" + b"\x00" * 100)

        mock_worker = MagicMock()
        mock_worker.convert_to_images.return_value = [
            str(tmp_path / "page_001.png"),
            str(tmp_path / "page_002.png"),
        ]
        mock_create_worker.return_value = mock_worker

        mock_llm = MagicMock()
        mock_llm.completion.side_effect = ["# Page 1", "# Page 2"]
        mock_llm_class.return_value = mock_llm

        png_data = b"\x89\x50\x4e\x47" + b"\x00" * 100
        result = convert_to_markdown(
            png_data,
            output_dir=str(tmp_path),
            cleanup=False,
        )

        assert "# Page 1" in result
        assert "# Page 2" in result
        assert mock_llm.completion.call_count == 2

    @patch("markpdfdown.main.LLMClient")
    @patch("markpdfdown.main.create_worker")
    def test_empty_images_raises(self, mock_create_worker, mock_llm_class, tmp_path):
        """Test empty images list raises ValueError"""
        mock_worker = MagicMock()
        mock_worker.convert_to_images.return_value = []
        mock_create_worker.return_value = mock_worker

        png_data = b"\x89\x50\x4e\x47" + b"\x00" * 100
        with pytest.raises(ValueError, match="Failed to convert file to images"):
            convert_to_markdown(
                png_data,
                output_dir=str(tmp_path),
                cleanup=False,
            )

    @patch("markpdfdown.main.LLMClient")
    @patch("markpdfdown.main.create_worker")
    @patch("markpdfdown.main.shutil.rmtree")
    def test_cleanup_removes_directory(
        self, mock_rmtree, mock_create_worker, mock_llm_class, tmp_path
    ):
        """Test cleanup=True removes output directory"""
        mock_worker = MagicMock()
        mock_worker.convert_to_images.return_value = [str(tmp_path / "image.png")]
        mock_create_worker.return_value = mock_worker

        mock_llm = MagicMock()
        mock_llm.completion.return_value = "# Content"
        mock_llm_class.return_value = mock_llm

        (tmp_path / "image.png").write_bytes(b"\x89PNG" + b"\x00" * 100)

        png_data = b"\x89\x50\x4e\x47" + b"\x00" * 100
        convert_to_markdown(
            png_data,
            output_dir="output/test_cleanup",
            cleanup=True,
        )

        mock_rmtree.assert_called_once_with("output/test_cleanup")

    @patch("markpdfdown.main.LLMClient")
    @patch("markpdfdown.main.create_worker")
    @patch("markpdfdown.main.shutil.rmtree")
    def test_cleanup_handles_exception(
        self, mock_rmtree, mock_create_worker, mock_llm_class, tmp_path
    ):
        """Test cleanup exception is handled gracefully"""
        mock_worker = MagicMock()
        mock_worker.convert_to_images.return_value = [str(tmp_path / "image.png")]
        mock_create_worker.return_value = mock_worker

        mock_llm = MagicMock()
        mock_llm.completion.return_value = "# Content"
        mock_llm_class.return_value = mock_llm

        mock_rmtree.side_effect = Exception("Cleanup error")

        (tmp_path / "image.png").write_bytes(b"\x89PNG" + b"\x00" * 100)

        png_data = b"\x89\x50\x4e\x47" + b"\x00" * 100
        # Should not raise despite cleanup error
        result = convert_to_markdown(
            png_data,
            output_dir="output/test_cleanup",
            cleanup=True,
        )
        assert "# Content" in result


class TestConvertFromFile:
    """Tests for convert_from_file function"""

    def test_nonexistent_file_raises(self):
        """Test nonexistent file raises ValueError"""
        with pytest.raises(ValueError, match="Input file not found"):
            convert_from_file("/nonexistent/file.pdf")

    @patch("markpdfdown.main.convert_to_markdown")
    def test_reads_file_and_converts(self, mock_convert, sample_image_path):
        """Test file is read and passed to convert_to_markdown"""
        mock_convert.return_value = "# Markdown"

        result = convert_from_file(sample_image_path)

        assert result == "# Markdown"
        mock_convert.assert_called_once()

        # Check the file data was read
        call_args = mock_convert.call_args
        assert len(call_args[0][0]) > 0  # input_data is not empty

    @patch("markpdfdown.main.convert_to_markdown")
    def test_passes_page_range(self, mock_convert, sample_image_path):
        """Test page range is passed to convert_to_markdown"""
        mock_convert.return_value = "# Markdown"

        convert_from_file(sample_image_path, start_page=2, end_page=5)

        call_kwargs = mock_convert.call_args.kwargs
        assert call_kwargs["start_page"] == 2
        assert call_kwargs["end_page"] == 5

    @patch("markpdfdown.main.convert_to_markdown")
    def test_passes_filename(self, mock_convert, sample_image_path):
        """Test filename is passed to convert_to_markdown"""
        mock_convert.return_value = "# Markdown"

        convert_from_file(sample_image_path)

        call_kwargs = mock_convert.call_args.kwargs
        assert call_kwargs["input_filename"] == os.path.basename(sample_image_path)


class TestConvertFromStdin:
    """Tests for convert_from_stdin function"""

    @patch("markpdfdown.main.convert_to_markdown")
    @patch("markpdfdown.main.sys.stdin")
    def test_reads_stdin_and_converts(self, mock_stdin, mock_convert):
        """Test stdin data is read and converted"""
        mock_convert.return_value = "# Stdin Content"
        mock_stdin.buffer.read.return_value = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
        mock_stdin.buffer.name = "<stdin>"

        result = convert_from_stdin()

        assert result == "# Stdin Content"
        mock_convert.assert_called_once()

    @patch("markpdfdown.main.sys.stdin")
    def test_empty_stdin_raises(self, mock_stdin):
        """Test empty stdin raises ValueError"""
        mock_stdin.buffer.read.return_value = b""

        with pytest.raises(ValueError, match="No input data received"):
            convert_from_stdin()

    @patch("markpdfdown.main.convert_to_markdown")
    @patch("markpdfdown.main.sys.stdin")
    def test_stdin_passes_none_filename(self, mock_stdin, mock_convert):
        """Test stdin passes None for input_filename"""
        mock_convert.return_value = "# Content"
        mock_stdin.buffer.read.return_value = b"\x89PNG" + b"\x00" * 100
        mock_stdin.buffer.name = "<stdin>"

        convert_from_stdin()

        call_kwargs = mock_convert.call_args.kwargs
        assert call_kwargs["input_filename"] is None
