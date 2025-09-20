"""
Base file worker and factory for different file types
"""

import logging
import os
from abc import ABC, abstractmethod

from .utils import validate_page_range

logger = logging.getLogger(__name__)


class FileWorker(ABC):
    """
    Abstract base class for file processing workers
    """

    def __init__(self, input_path: str):
        """
        Initialize file worker

        Args:
            input_path: Path to input file
        """
        self.input_path = input_path
        self.output_dir = os.path.dirname(input_path)

    @abstractmethod
    def convert_to_images(self, **kwargs) -> list[str]:
        """
        Convert input file to images

        Returns:
            List of generated image paths
        """
        pass


class PDFWorker(FileWorker):
    """
    Worker for processing PDF files
    """

    def __init__(self, input_path: str, start_page: int = 1, end_page: int = 0):
        super().__init__(input_path)

        try:
            import PyPDF2

            self.reader = PyPDF2.PdfReader(input_path)
            self.total_pages = len(self.reader.pages)
        except Exception as e:
            logger.error(f"Failed to read PDF file: {e}")
            raise ValueError(f"Invalid PDF file: {input_path}") from e

        # Validate and normalize page range
        self.start_page, self.end_page = validate_page_range(
            start_page, end_page, self.total_pages
        )

        logger.info(
            f"Processing PDF from page {self.start_page} to page {self.end_page}"
        )

        # Extract pages if needed
        if self.start_page != 1 or self.end_page != self.total_pages:
            extracted_path = self._extract_pages()
            if extracted_path:
                self.input_path = extracted_path
                logger.info("Page extraction completed")
            else:
                logger.warning("Page extraction failed, using original file")

    def _extract_pages(self) -> str:
        """
        Extract specified page range from PDF

        Returns:
            Path to extracted PDF file, empty string on failure
        """
        try:
            import PyPDF2

            writer = PyPDF2.PdfWriter()

            # Add pages (convert to 0-based index)
            for page_num in range(self.start_page - 1, self.end_page):
                writer.add_page(self.reader.pages[page_num])

            # Generate output filename
            base_name = os.path.basename(self.input_path).rsplit(".", 1)[0]
            output_name = f"{base_name}_pages_{self.start_page}-{self.end_page}.pdf"
            output_path = os.path.join(self.output_dir, output_name)

            # Write extracted PDF
            os.makedirs(self.output_dir, exist_ok=True)
            with open(output_path, "wb") as out_file:
                writer.write(out_file)

            return output_path

        except Exception as e:
            logger.error(f"Page extraction failed: {e}")
            return ""

    def convert_to_images(self, dpi: int = 300, fmt: str = "jpg") -> list[str]:
        """
        Convert PDF pages to images using PyMuPDF

        Args:
            dpi: Output image resolution
            fmt: Image format (jpg/png)

        Returns:
            List of generated image paths
        """
        try:
            import fitz  # PyMuPDF

            os.makedirs(self.output_dir, exist_ok=True)
            img_paths = []

            doc = fitz.open(self.input_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(dpi=dpi)
                output_path = os.path.join(
                    self.output_dir, f"page_{page_num + 1:04d}.{fmt}"
                )
                pix.save(output_path)
                img_paths.append(output_path)

            doc.close()
            return img_paths

        except Exception as e:
            logger.error(f"PDF to image conversion failed: {e}")
            return []


class ImageWorker(FileWorker):
    """
    Worker for processing image files
    """

    def __init__(self, input_path: str):
        super().__init__(input_path)
        logger.info(f"Processing image file: {input_path}")

    def convert_to_images(self) -> list[str]:
        """
        For image files, just return the original path

        Returns:
            List containing the original image path
        """
        return [self.input_path]


def create_worker(
    input_path: str, start_page: int = 1, end_page: int = 0
) -> FileWorker:
    """
    Create appropriate worker based on file extension

    Args:
        input_path: Path to input file
        start_page: Starting page number (for PDF)
        end_page: Ending page number (for PDF, 0 means last page)

    Returns:
        FileWorker instance

    Raises:
        ValueError: If file type is not supported
    """
    _, ext = os.path.splitext(input_path)
    ext = ext.lower()

    if ext == ".pdf":
        return PDFWorker(input_path, start_page, end_page)
    elif ext in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]:
        return ImageWorker(input_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
