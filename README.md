<div align="center">

<h1>MarkPDFDown</h1>
<p align="center">English | <a href="./README_zh.md">中文</a> | <a href="./README_ja.md">日本語</a> | <a href="./README_ru.md">Русский</a> | <a href="./README_fa.md">فارسی</a> | <a href="./README_ar.md">العربية</a></p>

[![Size]][hub_url]
[![Pulls]][hub_url]
[![Tag]][tag_url]
[![License]][license_url]
<p>A powerful tool that leverages multimodal large language models to transcribe PDF files into Markdown format.</p>

![markpdfdown](https://raw.githubusercontent.com/markpdfdown/markpdfdown/refs/heads/master/tests/markpdfdown.png)

</div>

## Overview

MarkPDFDown is designed to simplify the process of converting PDF documents into clean, editable Markdown text. By utilizing advanced multimodal AI models through LiteLLM, it can accurately extract text, preserve formatting, and handle complex document structures including tables, formulas, and diagrams.

## Features

- **PDF to Markdown Conversion**: Transform any PDF document into well-formatted Markdown
- **Image to Markdown Conversion**: Transform image into well-formatted Markdown
- **Multi-Provider Support**: Supports OpenAI and OpenRouter through LiteLLM
- **Flexible CLI**: Both file-based and pipe-based usage modes
- **Format Preservation**: Maintains headings, lists, tables, and other formatting elements
- **Page Range Selection**: Convert specific page ranges from PDF documents
- **Modular Architecture**: Clean, maintainable codebase with separation of concerns

## Demo
![](https://raw.githubusercontent.com/markpdfdown/markpdfdown/refs/heads/master/tests/demo_02.png)

## Installation

### Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/MarkPDFdown/markpdfdown.git
cd markpdfdown

# Install dependencies and create virtual environment
uv sync

# Install the package in development mode
uv pip install -e .
```

### Using conda

```bash
conda create -n markpdfdown python=3.9
conda activate markpdfdown

# Clone the repository
git clone https://github.com/MarkPDFdown/markpdfdown.git
cd markpdfdown

# Install dependencies
pip install -e .
```

## Configuration

MarkPDFDown uses environment variables for configuration. Create a `.env` file in your project directory:

```bash
# Copy the sample configuration
cp .env.sample .env
```

Edit the `.env` file with your settings:

```bash
# Model Configuration
MODEL_NAME=gpt-4o

# API Keys (LiteLLM automatically detects these)
OPENAI_API_KEY=your-openai-api-key
# or for OpenRouter
OPENROUTER_API_KEY=your-openrouter-api-key

# Optional Parameters
TEMPERATURE=0.3
MAX_TOKENS=8192
RETRY_TIMES=3
```

### Supported Models

#### OpenAI Models
```bash
MODEL_NAME=gpt-4o
MODEL_NAME=gpt-4o-mini
MODEL_NAME=gpt-4-vision-preview
```

#### OpenRouter Models
```bash
MODEL_NAME=openrouter/anthropic/claude-3.5-sonnet
MODEL_NAME=openrouter/google/gemini-pro-vision
MODEL_NAME=openrouter/meta-llama/llama-3.2-90b-vision
```

## Usage

### File Mode (Recommended)

```bash
# Basic conversion
markpdfdown --input document.pdf --output output.md

# Convert specific page range
markpdfdown --input document.pdf --output output.md --start 1 --end 10

# Convert image to markdown
markpdfdown --input image.png --output output.md

# Using python module
python -m markpdfdown --input document.pdf --output output.md
```

### Pipe Mode (Docker-friendly)

```bash
# PDF to markdown via pipe
markpdfdown < document.pdf > output.md

# Using python module
python -m markpdfdown < document.pdf > output.md
```

### Advanced Usage

```bash
# Convert pages 5-15 of a PDF
markpdfdown --input large_document.pdf --output chapter.md --start 5 --end 15

# Process multiple files
for file in *.pdf; do
    markpdfdown --input "$file" --output "${file%.pdf}.md"
done
```

## Docker Usage

```bash
# Build the image (if needed)
docker build -t markpdfdown .

# Run with environment variables
docker run -i \
  -e MODEL_NAME=gpt-4o \
  -e OPENAI_API_KEY=your-api-key \
  markpdfdown < input.pdf > output.md

# Using OpenRouter
docker run -i \
  -e MODEL_NAME=openrouter/anthropic/claude-3.5-sonnet \
  -e OPENROUTER_API_KEY=your-openrouter-key \
  markpdfdown < input.pdf > output.md
```

## Development Setup

### Code Quality Tools

This project uses `ruff` for linting and formatting, and `pre-commit` for automated code quality checks.

#### Install development dependencies

```bash
# If using uv
uv sync --group dev

# If using pip
pip install -e ".[dev]"
```

#### Set up pre-commit hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run pre-commit on all files (optional)
pre-commit run --all-files
```

#### Code formatting and linting

```bash
# Format code with ruff
ruff format

# Run linting checks
ruff check

# Fix auto-fixable issues
ruff check --fix
```

## Requirements
- Python 3.9+
- [uv](https://astral.sh/uv/) (recommended for package management) or conda/pip
- Dependencies specified in `pyproject.toml`
- Access to supported LLM providers (OpenAI or OpenRouter)

## Architecture

The project follows a modular architecture:

```
src/markpdfdown/
├── __init__.py          # Package initialization
├── __main__.py          # Entry point for python -m
├── cli.py               # Command line interface
├── main.py              # Core conversion logic
├── config.py            # Configuration management
└── core/                # Core modules
    ├── llm_client.py    # LiteLLM integration
    ├── file_worker.py   # File processing
    └── utils.py         # Utility functions
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch ( `git checkout -b feature/amazing-feature` )
3. Set up the development environment:
   ```bash
   uv sync --group dev
   pre-commit install
   ```
4. Make your changes and ensure code quality:
   ```bash
   ruff format
   ruff check --fix
   pre-commit run --all-files
   ```
5. Commit your changes ( `git commit -m 'feat: Add some amazing feature'` )
6. Push to the branch ( `git push origin feature/amazing-feature` )
7. Open a Pull Request

Please ensure your code follows the project's coding standards by running the linting and formatting tools before submitting.

## License
This project is licensed under the Apache License 2.0. See the LICENSE file for details.

## Acknowledgments
- Thanks to the developers of LiteLLM for providing unified LLM access
- Thanks to the developers of the multimodal AI models that power this tool
- Inspired by the need for better PDF to Markdown conversion tools

[hub_url]: https://hub.docker.com/r/jorbenzhu/markpdfdown/
[tag_url]: https://github.com/markpdfdown/markpdfdown/releases
[license_url]: https://github.com/markpdfdown/markpdfdown/blob/main/LICENSE

[Size]: https://img.shields.io/docker/image-size/jorbenzhu/markpdfdown/latest?color=066da5&label=size
[Pulls]: https://img.shields.io/docker/pulls/jorbenzhu/markpdfdown.svg?style=flat&label=pulls&logo=docker
[Tag]: https://img.shields.io/github/release/markpdfdown/markpdfdown.svg
[License]: https://img.shields.io/github/license/markpdfdown/markpdfdown