import os
import sys
import time
import shutil
import logging
from core import LLMClient, PDFWorker
import argparse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)


def completion(
    message,
    model="",
    system_prompt="",
    image_paths=None,
    temperature=0.5,
    max_tokens=8192,
    retry_times=3,
):
    """
    Call OpenAI's completion interface for text generation

    Args:
        message (str): User input message
        model (str): Model name
        system_prompt (str, optional): System prompt, defaults to empty string
        image_paths (List[str], optional): List of image paths, defaults to None
        temperature (float, optional): Temperature for text generation, defaults to 0.5
        max_tokens (int, optional): Maximum number of tokens for generated text, defaults to 8192
    Returns:
        str: Generated text content
    """

    # Get API key and API base URL from environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("Please set the OPENAI_API_KEY environment variables")
        exit(1)
    base_url = os.getenv("OPENAI_API_BASE")
    if not base_url:
        base_url = "https://api.openai.com/v1/"

    # If no model is specified, use the default model
    if not model:
        model = os.getenv("OPENAI_DEFAULT_MODEL")
        if not model:
            model = "gpt-4o"

    # Initialize LLMClient
    client = LLMClient.LLMClient(base_url=base_url, api_key=api_key, model=model)
    # Call completion method with retry mechanism
    for _ in range(retry_times):
        try:
            response = client.completion(
                user_message=message,
                system_prompt=system_prompt,
                image_paths=image_paths,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response
        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            # If retry fails, wait for a while before retrying
            time.sleep(0.5)
    return ""


def convert_image_to_markdown(image_path):
    """
    Convert image to Markdown format
    Args:
        image_path (str): Path to the image
    Returns:
        str: Converted Markdown string
    """
    user_prompt = """
    Please read the content in the image and transcribe it into pure Markdown format. Pay special attention to:
    1. Maintain the format of headings, text, formulas, and table rows and columns
    2. Output ONLY the pure Markdown content
    3. DO NOT wrap the content with ```markdown``` or any other code block markers
    4. DO NOT add any explanations or additional text
    """

    response = completion(
        message=user_prompt,
        model="",
        image_paths=[image_path],
        temperature=0.3,
        max_tokens=8192,
    )
    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF to Markdown")
    parser.add_argument("-i", "--input", help="Input PDF file path")
    parser.add_argument("-o", "--output", help="Output markdown file path")
    parser.add_argument(
        "pages", nargs="*", type=int, help="Page range (start_page [end_page])"
    )
    args = parser.parse_args()

    start_page = 1
    end_page = 0

    # Handle page range arguments
    if len(args.pages) > 1:
        start_page = args.pages[0]
        end_page = args.pages[1]
    elif len(args.pages) == 1:
        end_page = args.pages[0]

    # Handle input file
    input_data = None
    if args.input:
        with open(args.input, "rb") as f:
            input_data = f.read()
    else:
        input_data = sys.stdin.buffer.read()

    if not input_data:
        logger.error("No input data received")
        logger.error(
            "Usage: python main.py [-i input.pdf] [-o output.md] [start_page] [end_page]"
        )
        exit(1)

    # Create output directory
    output_dir = f"output/{time.strftime('%Y%m%d%H%M%S')}"
    os.makedirs(output_dir, exist_ok=True)

    # Save input PDF to output directory
    input_pdf_path = os.path.join(output_dir, "input.pdf")
    with open(input_pdf_path, "wb") as f:
        f.write(input_data)

    pdf_worker = PDFWorker.PDFWorker(input_pdf_path)
    total_pages = pdf_worker.get_total_pages()
    if start_page < 1 or start_page > total_pages:
        start_page = 1
    if end_page == 0 or end_page > total_pages:
        end_page = total_pages
    logger.info("Start processing from page %d to page %d", start_page, end_page)

    extract_path = input_pdf_path
    if start_page != 1 or end_page != total_pages:
        # Extract PDF content from specified page range
        extract_path = pdf_worker.extract_pages(start_page, end_page, output_dir)
        logger.info("Extract pages to %s", extract_path)

    # Convert PDF to images
    convert_worker = PDFWorker.PDFWorker(extract_path)
    img_paths = convert_worker.convert_to_images(output_dir=output_dir)
    logger.info("Image conversion completed")

    # Convert images to Markdown
    markdown = ""
    for img_path in sorted(img_paths):
        img_path = img_path.replace("\\", "/")
        logger.info("Converting image %s to Markdown", img_path)
        markdown += convert_image_to_markdown(img_path)
        markdown += "\n\n"
    logger.info("Image conversion to Markdown completed")

    # Output Markdown
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(markdown)
        logger.info("Markdown saved to %s", args.output)
    else:
        print(markdown)

    # Remove output path
    shutil.rmtree(output_dir)
    exit(0)
