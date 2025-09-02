import logging
import os
import shutil
import sys
import time

from dotenv import load_dotenv

from core import LLMClient
from core.FileWorker import create_worker
from core.Util import remove_markdown_warp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)

load_dotenv()


def completion(
    message,
    model="",
    system_prompt="",
    image_paths=None,
    temperature=0.5,
    max_tokens=8192,
    retry_times=3,
    reasoning_effort=None,
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
        retry_times (int, optional): Number of retries, defaults to 3
        reasoning_effort (str, optional): Reasoning effort, defaults to None
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
    
    if not reasoning_effort:
        reasoning_effort = os.getenv("OPENAI_REASONING_EFFORT")
        if not reasoning_effort:
            reasoning_effort = None

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
                reasoning_effort=reasoning_effort,
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

    response = completion(
        message=user_prompt,
        system_prompt=system_prompt,
        image_paths=[image_path],
        temperature=0.3,
        max_tokens=8192,
    )
    response = remove_markdown_warp(response, "markdown")
    return response


if __name__ == "__main__":
    start_page = 1
    end_page = 0
    if len(sys.argv) > 2:
        start_page = int(sys.argv[1])
        end_page = int(sys.argv[2])
    elif len(sys.argv) > 1:
        start_page = 1
        end_page = int(sys.argv[1])

    # Read binary data from standard input
    input_data = sys.stdin.buffer.read()
    if not input_data:
        logger.error("No input data received")
        logger.error(
            "Usage: python main.py [start_page] [end_page] < path_to_input.pdf"
        )
        exit(1)

    # Create output directory
    output_dir = f"output/{time.strftime('%Y%m%d%H%M%S')}"
    os.makedirs(output_dir, exist_ok=True)

    # Try to get extension from file name
    input_filename = os.path.basename(sys.stdin.buffer.name)
    input_ext = os.path.splitext(input_filename)[1]

    # If there is no extension or the file comes from standard input, try to determine the type by file content
    if not input_ext or input_filename == "<stdin>":
        # PDF file magic number/signature is %PDF-
        if input_data.startswith(b"%PDF-"):
            input_ext = ".pdf"
            logger.info("Recognized as PDF file by file content")
        # JPEG file magic number/signature is FF D8 FF DB
        elif input_data.startswith(b"\xff\xd8\xff\xdb"):
            input_ext = ".jpeg"
            logger.info("Recognized as JPEG file by file content")
        # JPG file magic number/signature is FF D8 FF E0
        elif input_data.startswith(b"\xff\xd8\xff\xe0"):
            input_ext = ".jpg"
            logger.info("Recognized as JPG file by file content")
        # PNG file magic number/signature is 89 50 4E 47
        elif input_data.startswith(b"\x89\x50\x4e\x47"):
            input_ext = ".png"
            logger.info("Recognized as PNG file by file content")
        # BMP file magic number/signature is 42 4D
        elif input_data.startswith(b"\x42\x4d"):
            input_ext = ".bmp"
            logger.info("Recognized as BMP file by file content")
        else:
            logger.error("Unsupported file type")
            exit(1)

    input_path = os.path.join(output_dir, f"input{input_ext}")
    with open(input_path, "wb") as f:
        f.write(input_data)

    # create file worker
    try:
        worker = create_worker(input_path, start_page, end_page)
    except ValueError as e:
        logger.error(str(e))
        exit(1)

    # convert to images
    img_paths = worker.convert_to_images()
    logger.info("Image conversion completed")

    # convert to markdown
    markdown = ""
    for img_path in sorted(img_paths):
        img_path = img_path.replace("\\", "/")
        logger.info("Converting image %s to Markdown", img_path)
        content = convert_image_to_markdown(img_path)
        if content:
            # 写入文件
            with open(
                os.path.join(output_dir, f"{os.path.basename(img_path)}.md"), "w"
            ) as f:
                f.write(content)
            markdown += content
            markdown += "\n\n"

    # Output Markdown
    print(markdown)
    logger.info("Image conversion to Markdown completed")
    # Remote output path
    shutil.rmtree(output_dir)
    exit(0)
