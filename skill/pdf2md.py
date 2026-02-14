#!/usr/bin/env python3
"""
PDF to Markdown Conversion Tool for Claude Code
This script extracts images from PDF pages for Claude Code to convert to Markdown.
"""

import sys
import os
from pathlib import Path
from typing import Optional, Tuple


# ============================================================================
# Utility functions (copied from markpdfdown to avoid dependency issues)
# ============================================================================

def detect_file_type(file_data: bytes, extension: str = None) -> Optional[str]:
    """
    Detect file type from binary data or extension.

    Args:
        file_data: Binary file data
        extension: File extension (optional)

    Returns:
        File type string (pdf, jpg, png, etc.) or None
    """
    if not file_data:
        return None

    # PDF file magic number
    if file_data.startswith(b"%PDF-"):
        return "pdf"

    # JPEG file magic numbers
    elif file_data.startswith(b"\xff\xd8\xff"):
        return "jpg"

    # PNG file magic number
    elif file_data.startswith(b"\x89\x50\x4e\x47"):
        return "png"

    # BMP file magic number
    elif file_data.startswith(b"\x42\x4d"):
        return "bmp"

    # GIF file magic number
    elif file_data.startswith(b"GIF87a") or file_data.startswith(b"GIF89a"):
        return "gif"

    # Fallback to extension if provided
    if extension:
        ext = extension.lower().lstrip('.')
        if ext in ['pdf', 'jpg', 'jpeg', 'png', 'bmp', 'gif']:
            return ext

    return None


def validate_page_range(
    start_page: int, end_page: Optional[int], total_pages: int
) -> Tuple[int, int]:
    """
    Validate and normalize page range.

    Args:
        start_page: Starting page number (1-based)
        end_page: Ending page number (1-based, None means last page)
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

    # Handle end_page = None (means last page)
    if end_page is None:
        end_page = total_pages

    if end_page < start_page:
        raise ValueError(f"End page {end_page} must be >= start page {start_page}")

    if end_page > total_pages:
        end_page = total_pages

    return start_page, end_page


def extract_pdf_images(
    pdf_path: str,
    output_dir: str,
    start_page: int = 1,
    end_page: Optional[int] = None,
    dpi: int = 300,
) -> Tuple[list[str], int]:
    """
    Extract images from PDF pages.

    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save extracted images
        start_page: Starting page number (1-based)
        end_page: Ending page number (1-based, None for last page)
        dpi: Resolution for image extraction

    Returns:
        Tuple of (list of image paths, total page count)
    """
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Validate PDF file exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    # Detect file type
    with open(pdf_path, "rb") as f:
        file_data = f.read()

    file_type = detect_file_type(file_data, Path(pdf_path).suffix)

    if file_type not in ["pdf", "jpg", "jpeg", "png", "bmp", "gif"]:
        raise ValueError(f"Unsupported file type: {file_type}")

    # Handle image files
    if file_type in ["jpg", "jpeg", "png", "bmp", "gif"]:
        # For image files, just return the original path
        return [pdf_path], 1

    # Handle PDF files
    try:
        import PyPDF2
    except ImportError:
        raise ImportError("PyPDF2 is required for PDF processing. Install with: pip install pypdf2")

    try:
        import fitz  # PyMuPDF
    except ImportError:
        raise ImportError("PyMuPDF is required for PDF to image conversion. Install with: pip install pymupdf")

    # Read PDF and get page count
    with open(pdf_path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        total_pages = len(pdf_reader.pages)

    # Validate and normalize page range
    start_page, end_page = validate_page_range(start_page, end_page, total_pages)

    # Extract specified pages
    pdf_writer = PyPDF2.PdfWriter()
    with open(pdf_path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page_num in range(start_page - 1, end_page):
            pdf_writer.add_page(pdf_reader.pages[page_num])

    # Save extracted pages to temporary file
    temp_pdf_path = output_path / "temp_extracted.pdf"
    with open(temp_pdf_path, "wb") as f:
        pdf_writer.write(f)

    # Convert pages to images using PyMuPDF
    doc = fitz.open(str(temp_pdf_path))
    image_paths = []

    for page_index in range(len(doc)):
        page = doc[page_index]
        # Render page to pixmap
        mat = fitz.Matrix(dpi / 72, dpi / 72)  # 72 is default DPI
        pix = page.get_pixmap(matrix=mat)

        # Generate output filename
        page_number = start_page + page_index
        image_filename = f"page_{page_number:04d}.jpg"
        image_path = output_path / image_filename

        # Save image
        pix.save(str(image_path), "jpeg")
        image_paths.append(str(image_path))

    doc.close()

    # Clean up temporary PDF
    if temp_pdf_path.exists():
        temp_pdf_path.unlink()

    return image_paths, total_pages


def main():
    """Main entry point for the script."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract images from PDF for Claude Code conversion"
    )
    parser.add_argument(
        "input",
        help="Input PDF file path"
    )
    parser.add_argument(
        "--output-dir",
        default="./pdf_images",
        help="Output directory for extracted images (default: ./pdf_images)"
    )
    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="Start page number (1-based, default: 1)"
    )
    parser.add_argument(
        "--end",
        type=int,
        default=None,
        help="End page number (1-based, default: last page)"
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Image resolution (default: 300)"
    )

    args = parser.parse_args()

    try:
        image_paths, total_pages = extract_pdf_images(
            args.input,
            args.output_dir,
            args.start,
            args.end,
            args.dpi,
        )

        print(f"Successfully extracted {len(image_paths)} images from {total_pages} pages")
        print(f"Images saved to: {args.output_dir}")
        print("\nExtracted images:")
        for i, img_path in enumerate(image_paths, 1):
            print(f"  {i}. {img_path}")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
