"""
Main conversion logic for MarkPDFDown
"""

import logging
import os
import shutil
import sys
import time
from typing import Optional

from .config import config
from .core.file_worker import create_worker
from .core.llm_client import LLMClient
from .core.utils import detect_file_type, remove_markdown_wrap

logger = logging.getLogger(__name__)


def convert_image_to_markdown(image_path: str, llm_client: LLMClient) -> str:
    """
    Convert a single image to Markdown format

    Args:
        image_path: Path to the image file
        llm_client: LLM client instance

    Returns:
        Converted Markdown content
    """
    system_prompt = """
You are a helpful assistant that can convert images to Markdown format. You are given an image, and you need to convert it to Markdown format. Please output the Markdown content only, without any other text.
"""

    user_prompt = """
Below is the image of one page of a document, please read the content in the image and transcribe it into plain Markdown format. Please note:
1. Identify heading levels, text styles, formulas, and the format of table rows and columns
2. Mathematical formulas should be transcribed using LaTeX syntax, ensuring consistency with the original
3. Please output the Markdown content only, without any other text.

Output Example:
```markdown
{example}
```
"""

    try:
        response = llm_client.completion(
            user_message=user_prompt,
            system_prompt=system_prompt,
            image_paths=[image_path],
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            retry_times=config.retry_times,
        )

        # Remove markdown wrapper if present
        response = remove_markdown_wrap(response, "markdown")
        return response

    except Exception as e:
        logger.error(f"Failed to convert image {image_path}: {e}")
        return ""


def convert_to_markdown(
    input_data: bytes,
    start_page: int = 1,
    end_page: int = 0,
    input_filename: Optional[str] = None,
    output_dir: Optional[str] = None,
    cleanup: bool = True,
) -> str:
    """
    Convert PDF or image data to Markdown format

    Args:
        input_data: Binary file data
        start_page: Starting page number (1-based)
        end_page: Ending page number (1-based, 0 means last page)
        input_filename: Original filename (for type detection)
        output_dir: Output directory (if None, creates temporary directory)
        cleanup: Whether to clean up temporary files

    Returns:
        Converted Markdown content

    Raises:
        ValueError: If input data is invalid or unsupported
    """
    if not input_data:
        raise ValueError("No input data provided")

    # Create output directory
    if output_dir is None:
        output_dir = f"output/{time.strftime('%Y%m%d%H%M%S')}"
    os.makedirs(output_dir, exist_ok=True)

    # Detect file type
    input_ext = None
    if input_filename:
        input_ext = os.path.splitext(input_filename)[1].lower()

    # If no extension or unknown, detect from content
    if not input_ext or input_ext not in [
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".gif",
    ]:
        input_ext = detect_file_type(input_data)
        if not input_ext:
            raise ValueError("Unsupported file type")
        logger.info(f"Detected file type: {input_ext}")

    # Save input data to temporary file
    input_path = os.path.join(output_dir, f"input{input_ext}")
    with open(input_path, "wb") as f:
        f.write(input_data)

    try:
        # Create file worker
        worker = create_worker(input_path, start_page, end_page)

        # Convert to images
        img_paths = worker.convert_to_images()
        if not img_paths:
            raise ValueError("Failed to convert file to images")

        logger.info(f"Generated {len(img_paths)} images")

        # Initialize LLM client
        llm_client = LLMClient(config.model_name)

        # Convert images to markdown
        markdown_parts = []
        for img_path in sorted(img_paths):
            logger.info(f"Converting image: {os.path.basename(img_path)}")
            content = convert_image_to_markdown(img_path, llm_client)
            if content:
                # Save individual page markdown (optional)
                page_md_path = os.path.join(
                    output_dir, f"{os.path.basename(img_path)}.md"
                )
                with open(page_md_path, "w", encoding="utf-8") as f:
                    f.write(content)

                markdown_parts.append(content)

        # Combine all markdown content
        final_markdown = "\n\n".join(markdown_parts)

        logger.info("Conversion completed successfully")
        return final_markdown

    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        raise

    finally:
        # Cleanup temporary files if requested
        if cleanup and output_dir.startswith("output/"):
            try:
                shutil.rmtree(output_dir)
                logger.debug(f"Cleaned up temporary directory: {output_dir}")
            except Exception as e:
                logger.warning(f"Failed to cleanup directory {output_dir}: {e}")


def convert_from_stdin() -> str:
    """
    Convert file data from stdin to Markdown

    Returns:
        Converted Markdown content
    """
    # Read binary data from stdin
    input_data = sys.stdin.buffer.read()
    if not input_data:
        raise ValueError("No input data received from stdin")

    # Try to get filename from stdin (may not be available)
    input_filename = getattr(sys.stdin.buffer, "name", "<stdin>")
    if input_filename == "<stdin>":
        input_filename = None

    return convert_to_markdown(input_data, input_filename=input_filename)


def convert_from_file(input_path: str, start_page: int = 1, end_page: int = 0) -> str:
    """
    Convert file to Markdown

    Args:
        input_path: Path to input file
        start_page: Starting page number
        end_page: Ending page number

    Returns:
        Converted Markdown content
    """
    if not os.path.exists(input_path):
        raise ValueError(f"Input file not found: {input_path}")

    # Read file data
    with open(input_path, "rb") as f:
        input_data = f.read()

    return convert_to_markdown(
        input_data,
        start_page=start_page,
        end_page=end_page,
        input_filename=os.path.basename(input_path),
        cleanup=True,
    )
