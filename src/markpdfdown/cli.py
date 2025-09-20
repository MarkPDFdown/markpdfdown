"""
Command line interface for MarkPDFDown
"""

import argparse
import logging
import sys

from . import __version__
from .main import convert_from_file, convert_from_stdin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """
    Create command line argument parser

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog="markpdfdown",
        description="Convert PDF files and images to Markdown format using multimodal LLMs",
        epilog="Examples:\n"
        "  markpdfdown --input file.pdf --output output.md\n"
        "  markpdfdown --input file.pdf --output output.md --start 1 --end 10\n"
        "  markpdfdown < input.pdf > output.md\n"
        "  python -m markpdfdown --input image.png --output output.md",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Input/Output arguments
    parser.add_argument(
        "--input", "-i", type=str, help="Input file path (PDF or image)"
    )

    parser.add_argument("--output", "-o", type=str, help="Output Markdown file path")

    # Page range arguments (for PDF files)
    parser.add_argument(
        "--start", type=int, default=1, help="Starting page number (default: 1)"
    )

    parser.add_argument(
        "--end",
        type=int,
        default=0,
        help="Ending page number (default: 0, means last page)",
    )

    # Version argument
    parser.add_argument(
        "--version", action="version", version=f"markpdfdown {__version__}"
    )

    return parser


def validate_args(args: argparse.Namespace) -> None:
    """
    Validate command line arguments

    Args:
        args: Parsed command line arguments

    Raises:
        SystemExit: If arguments are invalid
    """
    # Check if both input and output are provided or both are missing
    has_input = args.input is not None
    has_output = args.output is not None

    if has_input != has_output:
        if has_input and not has_output:
            logger.error("Output file must be specified when input file is provided")
            sys.exit(1)
        elif has_output and not has_input:
            logger.error("Input file must be specified when output file is provided")
            sys.exit(1)

    # Validate page range
    if args.start < 1:
        logger.error("Start page must be >= 1")
        sys.exit(1)

    if args.end != 0 and args.end < args.start:
        logger.error(f"End page ({args.end}) must be >= start page ({args.start})")
        sys.exit(1)


def main() -> None:
    """
    Main CLI entry point
    """
    parser = create_parser()
    args = parser.parse_args()

    # Validate arguments
    validate_args(args)

    try:
        # Determine operation mode
        if args.input and args.output:
            # File mode: read from input file, write to output file
            logger.info(f"Converting {args.input} to {args.output}")
            if args.start != 1 or args.end != 0:
                logger.info(
                    f"Page range: {args.start} to {args.end if args.end != 0 else 'last'}"
                )

            markdown_content = convert_from_file(
                input_path=args.input, start_page=args.start, end_page=args.end
            )

            # Write output
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(markdown_content)

            logger.info(f"Conversion completed. Output saved to: {args.output}")

        else:
            # Pipe mode: read from stdin, write to stdout
            logger.info("Reading from stdin, writing to stdout")

            markdown_content = convert_from_stdin()

            # Write to stdout
            print(markdown_content)

            logger.info("Conversion completed")

    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
