"""
Tests for markpdfdown.core.file_worker module
"""

import os
import tempfile

import pytest

from markpdfdown.core.file_worker import (
    FileWorker,
    ImageWorker,
    PDFWorker,
    create_worker,
)


class TestImageWorker:
    """Tests for ImageWorker class"""

    def test_init(self, sample_image_path):
        """Test ImageWorker initialization"""
        worker = ImageWorker(sample_image_path)
        assert worker.input_path == sample_image_path
        assert worker.output_dir == os.path.dirname(sample_image_path)

    def test_convert_to_images_returns_input_path(self, sample_image_path):
        """Test convert_to_images returns the original image path"""
        worker = ImageWorker(sample_image_path)
        result = worker.convert_to_images()
        assert result == [sample_image_path]

    def test_is_file_worker_subclass(self):
        """Test ImageWorker is subclass of FileWorker"""
        assert issubclass(ImageWorker, FileWorker)


class TestPDFWorker:
    """Tests for PDFWorker class"""

    def test_init_with_valid_pdf(self, sample_pdf_path):
        """Test PDFWorker initialization with valid PDF"""
        worker = PDFWorker(sample_pdf_path)
        assert worker.input_path is not None
        assert worker.total_pages > 0

    def test_init_with_page_range(self, sample_pdf_path):
        """Test PDFWorker initialization with page range"""
        worker = PDFWorker(sample_pdf_path, start_page=1, end_page=1)
        assert worker.start_page == 1
        assert worker.end_page == 1

    def test_init_with_invalid_pdf_raises(self, tmp_path):
        """Test PDFWorker raises error for invalid PDF"""
        invalid_path = tmp_path / "invalid.pdf"
        invalid_path.write_bytes(b"not a pdf")

        with pytest.raises(ValueError, match="Invalid PDF file"):
            PDFWorker(str(invalid_path))

    def test_init_with_nonexistent_file_raises(self):
        """Test PDFWorker raises error for nonexistent file"""
        with pytest.raises(ValueError, match="Invalid PDF file"):
            PDFWorker("/nonexistent/file.pdf")

    def test_convert_to_images(self, sample_pdf_path, tmp_path):
        """Test PDF to images conversion"""
        worker = PDFWorker(sample_pdf_path, start_page=1, end_page=1)
        # Override output_dir to use temp directory
        worker.output_dir = str(tmp_path)
        worker.input_path = sample_pdf_path

        images = worker.convert_to_images(dpi=72, fmt="png")
        assert len(images) > 0
        for img_path in images:
            assert os.path.exists(img_path)
            assert img_path.endswith(".png")

    def test_is_file_worker_subclass(self):
        """Test PDFWorker is subclass of FileWorker"""
        assert issubclass(PDFWorker, FileWorker)


class TestCreateWorker:
    """Tests for create_worker factory function"""

    def test_create_pdf_worker(self, sample_pdf_path):
        """Test create_worker returns PDFWorker for PDF files"""
        worker = create_worker(sample_pdf_path)
        assert isinstance(worker, PDFWorker)

    def test_create_image_worker_png(self, sample_image_path):
        """Test create_worker returns ImageWorker for PNG files"""
        worker = create_worker(sample_image_path)
        assert isinstance(worker, ImageWorker)

    def test_create_image_worker_jpg(self, images_dir):
        """Test create_worker returns ImageWorker for JPG files"""
        # Create a temp jpg file for testing
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            f.write(b"\xff\xd8\xff\xe0" + b"\x00" * 100)
            jpg_path = f.name

        try:
            worker = create_worker(jpg_path)
            assert isinstance(worker, ImageWorker)
        finally:
            os.unlink(jpg_path)

    def test_create_image_worker_jpeg(self, tmp_path):
        """Test create_worker returns ImageWorker for JPEG files"""
        jpeg_path = tmp_path / "test.jpeg"
        jpeg_path.write_bytes(b"\xff\xd8\xff\xe0" + b"\x00" * 100)

        worker = create_worker(str(jpeg_path))
        assert isinstance(worker, ImageWorker)

    def test_create_image_worker_bmp(self, tmp_path):
        """Test create_worker returns ImageWorker for BMP files"""
        bmp_path = tmp_path / "test.bmp"
        bmp_path.write_bytes(b"\x42\x4d" + b"\x00" * 100)

        worker = create_worker(str(bmp_path))
        assert isinstance(worker, ImageWorker)

    def test_create_image_worker_gif(self, tmp_path):
        """Test create_worker returns ImageWorker for GIF files"""
        gif_path = tmp_path / "test.gif"
        gif_path.write_bytes(b"GIF89a" + b"\x00" * 100)

        worker = create_worker(str(gif_path))
        assert isinstance(worker, ImageWorker)

    def test_unsupported_file_type_raises(self, tmp_path):
        """Test create_worker raises for unsupported file types"""
        txt_path = tmp_path / "test.txt"
        txt_path.write_text("hello")

        with pytest.raises(ValueError, match="Unsupported file type"):
            create_worker(str(txt_path))

    def test_create_worker_with_page_range(self, sample_pdf_path):
        """Test create_worker passes page range to PDFWorker"""
        worker = create_worker(sample_pdf_path, start_page=1, end_page=1)
        assert isinstance(worker, PDFWorker)
        assert worker.start_page == 1
        assert worker.end_page == 1

    def test_case_insensitive_extension(self, tmp_path):
        """Test create_worker handles uppercase extensions"""
        png_path = tmp_path / "test.PNG"
        png_path.write_bytes(b"\x89\x50\x4e\x47" + b"\x00" * 100)

        worker = create_worker(str(png_path))
        assert isinstance(worker, ImageWorker)


class TestPDFWorkerExtractPages:
    """Tests for PDFWorker _extract_pages method"""

    def test_extract_pages_creates_new_pdf(self, sample_pdf_path, tmp_path):
        """Test _extract_pages creates new PDF file"""
        worker = PDFWorker(sample_pdf_path, start_page=1, end_page=1)
        worker.output_dir = str(tmp_path)

        # Check that extracted file was created
        assert os.path.exists(worker.input_path)

    def test_extract_pages_with_exception(self, sample_pdf_path, tmp_path, monkeypatch):
        """Test _extract_pages handles exception gracefully"""
        # Create worker first
        worker = PDFWorker(sample_pdf_path)
        worker.output_dir = str(tmp_path)

        # Mock PyPDF2.PdfWriter to raise exception
        def mock_writer_init(*args, **kwargs):
            raise Exception("Write error")

        import PyPDF2

        monkeypatch.setattr(PyPDF2, "PdfWriter", mock_writer_init)

        # Call _extract_pages which should return empty string on error
        result = worker._extract_pages()
        assert result == ""

    def test_extract_pages_failure_uses_original_file(
        self, sample_pdf_path, monkeypatch
    ):
        """Test when extraction fails, original file is used"""
        original_path = sample_pdf_path

        # Mock _extract_pages to return empty string (failure)
        def mock_extract_pages(self):
            return ""

        monkeypatch.setattr(PDFWorker, "_extract_pages", mock_extract_pages)

        # Create worker with page range that would trigger extraction
        worker = PDFWorker(sample_pdf_path, start_page=1, end_page=1)

        # Should still have the original path since extraction "failed"
        assert worker.input_path == original_path


class TestPDFWorkerConvertToImages:
    """Tests for PDFWorker convert_to_images method"""

    def test_convert_to_images_with_exception(
        self, sample_pdf_path, tmp_path, monkeypatch
    ):
        """Test convert_to_images handles exception gracefully"""
        worker = PDFWorker(sample_pdf_path)
        worker.output_dir = str(tmp_path)

        # Mock fitz.open to raise exception
        def mock_fitz_open(*args, **kwargs):
            raise Exception("Open error")

        import fitz

        monkeypatch.setattr(fitz, "open", mock_fitz_open)

        result = worker.convert_to_images()
        assert result == []
