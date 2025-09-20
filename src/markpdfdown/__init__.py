"""
MarkPDFDown - A powerful tool that leverages multimodal large language models
to transcribe PDF files into Markdown format.
"""

__version__ = "1.1.2"
__author__ = "MarkPDFDown Team"
__email__ = "jorbenzhu@gmail.com"
__description__ = "Convert PDF and images to Markdown using multimodal LLMs"

from .main import convert_to_markdown

__all__ = ["convert_to_markdown", "__version__"]
