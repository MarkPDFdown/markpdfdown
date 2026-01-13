# AGENTS.md

This file provides guidelines for AI agents working in this repository.

## Project Overview

**markpdfdown** - A tool that converts PDF documents and images to Markdown format using LLM vision capabilities. The project is built with Python 3.9+, uses `uv` for package management, `ruff` for linting/formatting, and `pytest` for testing.

## Build, Lint, and Test Commands

All commands should be run from the project root directory.

### Installation

```bash
make install    # Install dependencies with uv sync
```

### Development Tools

```bash
make format     # Format code with ruff format
make lint       # Run ruff check (no auto-fix)
make fix        # Auto-fix linting issues with ruff
make check      # Run all pre-commit hooks on all files
make update     # Update lock file and pre-commit hooks
```

### Testing

```bash
make test       # Run all tests with pytest
uv run pytest   # Alternative: run tests with uv
uv run pytest tests/test_file.py  # Run specific test file
uv run pytest -v tests/test_file.py::test_function_name  # Run single test
uv run pytest -k "test_name"  # Run tests matching pattern
```

Note: Test files should be placed in the `tests/` directory. Test fixtures (sample PDFs, images, expected outputs) are in `tests/cases/`.

## Code Style Guidelines

### Imports

Organize imports in three sections separated by blank lines:
1. Standard library imports
2. Third-party imports
3. Local application imports

```python
import logging
import os
from typing import Optional

import litellm

from markpdfdown.core import FileWorker
```

Use relative imports for intra-package imports:
```python
from .core.file_worker import FileWorker, PDFWorker, ImageWorker
from .core.llm_client import LLMClient
```

### Formatting

- **Line length**: 88 characters (ruff default)
- **Indent style**: Spaces (4 spaces per level)
- **Quote style**: Double quotes
- **Trailing whitespace**: None
- **EOF**: Final newline required

Use `make format` to auto-format code.

### Type Annotations

Use Python type hints for function signatures:
```python
def completion(
    self,
    user_message: str,
    system_prompt: Optional[str] = None,
    image_paths: Optional[list[str]] = None,
    temperature: float = 0.3,
    max_tokens: int = 8192,
    retry_times: int = 3,
) -> str:
```

Avoid `Union` in favor of `|` syntax (e.g., `str | None`), but note that `UP007` (use `X | Y` for type annotations) is ignored in the ruff config.

### Naming Conventions

- **Classes**: PascalCase (e.g., `PDFWorker`, `LLMClient`)
- **Functions and variables**: snake_case (e.g., `convert_to_images`, `input_path`)
- **Modules/Files**: snake_case (e.g., `file_worker.py`, `llm_client.py`)
- **Constants**: UPPER_SNAKE_CASE
- **Private methods/variables**: Prefix with underscore (e.g., `_encode_image`)

### Docstrings

Write docstrings for all public functions, methods, and classes:

```python
def remove_markdown_wrap(text: str, language: str = "markdown") -> str:
    """
    Remove markdown code block wrapper from text

    Args:
        text: The input text to process
        language: The markdown language tag to remove

    Returns:
        str: The processed text with markdown fences removed
    """
```

### Error Handling

- Use try/except blocks with specific exception types when possible
- Log errors using the module logger before re-raising or returning
- Use `logger.error(f"message: {str(e)}")` for error logging
- Define module-level logger at the top of each file:

```python
import logging

logger = logging.getLogger(__name__)
```

### Logging Configuration

Use `logging.basicConfig` in the main entry point:

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
```

Use parameterized logging in functions:
```python
logger.info("Processing PDF from page %d to page %d", start_page, end_page)
```

### File Structure

```
markpdfdown/
├── src/markpdfdown/       # Source code (src layout)
│   ├── __init__.py        # Package init with version
│   ├── __main__.py        # Module entry point
│   ├── cli.py             # CLI entry point
│   ├── config.py          # Configuration
│   ├── main.py            # Core conversion functions
│   └── core/              # Core implementation
│       ├── __init__.py    # Core module exports
│       ├── file_worker.py # FileWorker, PDFWorker, ImageWorker, create_worker
│       ├── llm_client.py  # LLMClient for API calls
│       └── utils.py       # Utility functions
├── tests/
│   └── cases/             # Test fixtures (images, PDFs, expected outputs)
└── pyproject.toml         # Project configuration
```

### Pre-commit Hooks

Before committing, run `make check` to ensure all files pass pre-commit validation:
- ruff (format + lint with auto-fix)
- trailing-whitespace
- end-of-file-fixer
- check-yaml
- check-toml
- check-merge-conflict
- check-added-large-files

### Dependency Management

- Add production dependencies to `dependencies` in `pyproject.toml`
- Add development dependencies to `dev` in `dependency-groups`
- Run `make update` to refresh lock file and pre-commit hooks

### General Patterns

1. **Factory pattern**: Use `create_worker()` function in `file_worker.py` to instantiate appropriate worker class based on file type
2. **Base classes**: Define abstract interfaces in `FileWorker` (ABC) with abstract methods
3. **Error messages**: Include file paths and specific error context in error messages
4. **File handling**: Use context managers (`with open(...)`) for file operations
5. **Path handling**: Use `os.path` for cross-platform path operations
6. **Src layout**: Project uses `src/markpdfdown/` layout for package source code
