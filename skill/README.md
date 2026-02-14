# PDF to Markdown Claude Code Skill

A Claude Code skill for converting PDF files to Markdown format using Claude's native vision capabilities.

## Overview

This skill enables Claude Code to convert PDF documents into well-formatted Markdown without relying on external LLM APIs. It leverages:
- **Existing PDF processing code** from the markpdfdown library
- **Claude's vision capabilities** to analyze and convert page images
- **Interactive conversion** with Claude Code handling the entire process

## Features

- ✅ **No External API Required**: Uses Claude Code's built-in vision instead of calling external LLMs
- ✅ **Full PDF Support**: Handles multi-page PDFs with page range selection
- ✅ **High Quality**: Preserves document structure, tables, math formulas, and code blocks
- ✅ **Customizable**: Adjust DPI, page ranges, and output locations
- ✅ **Interactive**: Claude Code guides you through the conversion process

## Installation

### Prerequisites

Make sure you have the required Python packages installed:

```bash
pip install pymupdf pypdf2
```

Or install from the parent project:

```bash
cd ..
pip install -e .
```

### Skill Setup

1. Copy the `skill` folder to your Claude Code skills directory, or use it directly from this repository

2. Ensure the skill has access to the markpdfdown source code (the `pdf2md.py` script imports from `../src/markpdfdown`)

## Usage

### Basic Usage

In Claude Code, use the skill to convert a PDF:

```
/pdf2md document.pdf
```

This will:
1. Extract all pages from `document.pdf` as images
2. Convert each page to Markdown using Claude's vision
3. Combine all pages into a single Markdown file
4. Save the output as `document.md`

### With Options

**Convert specific pages:**
```
/pdf2md research_paper.pdf --start 1 --end 10
```

**Custom output file:**
```
/pdf2md slides.pdf --output my_notes.md
```

**Higher resolution:**
```
/pdf2md document.pdf --dpi 600
```

**All options combined:**
```
/pdf2md book.pdf --start 5 --end 20 --output chapter1.md --dpi 300
```

## How It Works

### Architecture

```
User Input (PDF file)
    ↓
pdf2md.py (extraction script)
    ↓
PDF Pages → High-res Images (JPG)
    ↓
Claude Code (vision analysis)
    ↓
Image → Markdown (per page)
    ↓
Combined Markdown Document
    ↓
Output File (.md)
```

### Workflow

1. **PDF Extraction**:
   - The `pdf2md.py` script uses `file_worker.py` from the main library
   - Converts PDF pages to high-resolution JPG images (default 300 DPI)
   - Saves images to a temporary directory

2. **Image Analysis**:
   - Claude Code reads each extracted image
   - Analyzes content using vision capabilities
   - Converts to Markdown following detailed guidelines

3. **Markdown Generation**:
   - Preserves document structure (headings, lists, tables)
   - Converts math to LaTeX (`$inline$` and `$$block$$`)
   - Formats code blocks with language tags
   - Maintains text formatting (bold, italic, code)

4. **Output**:
   - Combines all page Markdown with proper spacing
   - Saves to specified output file
   - Optionally cleans up temporary images

## Conversion Guidelines

The skill follows comprehensive Markdown conversion rules defined in `skill_main.md`:

### Supported Elements

| Element | Example Output |
|---------|---------------|
| Headings | `# Title`, `## Section`, `### Subsection` |
| Text Formatting | `**bold**`, `*italic*`, `` `code` `` |
| Lists | `- item` or `1. item` (with nesting) |
| Tables | Markdown table format with alignment |
| Math | `$E=mc^2$` (inline), `$$...$$` (block) |
| Code Blocks | ````python ... ``` ```` |
| Images | `![alt](url)` or descriptive text |
| Footnotes | `[^1]` with definitions |

### Quality Standards

- **Accuracy**: All text captured precisely
- **Structure**: Logical document hierarchy preserved
- **Formatting**: Consistent Markdown style
- **Completeness**: No content omitted (except decorative elements)

## File Structure

```
skill/
├── README.md                 # This file
├── skill.json                # Skill metadata (JSON format)
├── skill.yaml                # Skill metadata (YAML format)
├── skill_main.md             # Main skill prompt with workflow
├── prompt.md                 # Detailed conversion guidelines
├── conversion_prompt.md      # Quick reference guide
└── pdf2md.py                 # PDF extraction utility script
```

## Dependencies

This skill reuses code from the parent markpdfdown library:

- `src/markpdfdown/core/file_worker.py` - PDF and image processing
- `src/markpdfdown/core/utils.py` - File type detection and validation

Required Python packages:
- `pymupdf` (fitz) - PDF to image conversion
- `pypdf2` - PDF page extraction
- `pathlib` - Path handling (built-in)

## Examples

### Example 1: Research Paper

Input: `research_paper.pdf` (15 pages)

```
/pdf2md research_paper.pdf --start 1 --end 15
```

Output: `research_paper.md` with:
- Title and abstract
- Section headings (Introduction, Methods, Results, etc.)
- Math formulas in LaTeX
- Tables formatted as Markdown
- References as a numbered list

### Example 2: Technical Documentation

Input: `api_docs.pdf` (50 pages)

```
/pdf2md api_docs.pdf --start 10 --end 25 --output api_reference.md
```

Output: `api_reference.md` with:
- API endpoint descriptions
- Code examples with syntax highlighting
- Parameter tables
- Example requests/responses

### Example 3: Presentation Slides

Input: `slides.pdf` (30 slides)

```
/pdf2md slides.pdf --output presentation_notes.md
```

Output: `presentation_notes.md` with:
- Each slide as a section
- Bullet points preserved
- Images described textually
- Code snippets formatted

## Troubleshooting

### Common Issues

**Issue**: "PDF file not found"
- **Solution**: Check the file path is correct and the file exists

**Issue**: "Unsupported file type"
- **Solution**: Ensure the file is a valid PDF or supported image format (JPG, PNG, BMP, GIF)

**Issue**: "Invalid page range"
- **Solution**: Check that start/end page numbers are within the document's page count

**Issue**: Images not displaying
- **Solution**: Verify the temporary image directory is accessible and has write permissions

### Debug Mode

To see detailed extraction info:

```bash
# Run the extraction script directly
python3 skill/pdf2md.py document.pdf --output-dir ./debug_images
```

This will show:
- Total pages extracted
- Image file paths
- Any extraction errors

## Customization

### Adjusting DPI

Higher DPI = better quality but larger files and slower processing:
- **150 DPI**: Fast, lower quality, smaller files
- **300 DPI**: Balanced (default)
- **600 DPI**: High quality, larger files, slower

### Modifying Conversion Rules

Edit `skill_main.md` or `conversion_prompt.md` to customize how Claude converts content:
- Change heading level logic
- Adjust table formatting
- Modify math formula handling
- Add custom patterns for specific document types

### Adding Post-Processing

You can add custom post-processing steps in the skill workflow:
- Auto-generate table of contents
- Add metadata headers
- Clean up specific formatting patterns
- Validate Markdown syntax

## Comparison with Main Library

| Feature | Main Library (markpdfdown) | This Skill |
|---------|---------------------------|------------|
| LLM Backend | External API (OpenAI, OpenRouter, etc.) | Claude Code (built-in) |
| API Key Required | ✅ Yes | ❌ No |
| Offline Use | ❌ No | ✅ Yes (if Claude Code is available) |
| Cost | Pay per API call | Free (part of Claude Code usage) |
| Customization | Config file | Interactive with Claude |
| Batch Processing | ✅ Yes (CLI) | Manual (interactive) |

## Contributing

This skill is part of the markpdfdown project. To contribute:

1. Test the skill with various PDF types
2. Report issues or suggest improvements
3. Submit pull requests with enhancements

## License

This skill inherits the license from the parent markpdfdown project.

## Credits

Built on top of:
- **markpdfdown**: The original PDF to Markdown converter
- **PyMuPDF**: PDF rendering engine
- **Claude Code**: Anthropic's AI-powered coding assistant

## Support

For issues or questions:
1. Check this README
2. Review the skill prompt files
3. Test with the standalone script: `python3 skill/pdf2md.py --help`
4. Report issues to the markpdfdown project

---

**Happy Converting! 📄 → 📝**
