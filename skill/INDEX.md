# PDF to Markdown Skill - File Index

This directory contains a Claude Code skill for converting PDF files to Markdown format.

## File Structure

```
skill/
├── INDEX.md                    # This file - overview of all files
├── README.md                   # Main documentation and installation guide
├── USAGE_GUIDE.md              # Detailed usage examples and workflows
│
├── skill.json                  # Skill metadata (JSON format)
├── skill.yaml                  # Skill metadata (YAML format)
│
├── skill_main.md               # Main skill prompt with complete workflow
├── prompt.md                   # Detailed conversion guidelines for Claude
├── conversion_prompt.md        # Quick reference guide for Markdown conversion
│
├── pdf2md.py                   # PDF extraction utility (standalone)
└── example_usage.sh            # Example shell script demonstrating usage
```

## Quick Reference

| File | Purpose | When to Use |
|------|---------|-------------|
| **README.md** | Main documentation | Start here for overview and setup |
| **USAGE_GUIDE.md** | Detailed examples | Learn how to use the skill in practice |
| **skill_main.md** | Main skill prompt | Reference for the complete workflow |
| **conversion_prompt.md** | Quick guide | Quick lookup for Markdown syntax |
| **pdf2md.py** | Extraction script | Run this to extract PDF pages to images |
| **example_usage.sh** | Example script | See working examples |

## Getting Started

1. **Read:** Start with `README.md`
2. **Install:** `pip install pymupdf pypdf2`
3. **Extract:** Run `python3 pdf2md.py your_file.pdf --output-dir ./images`
4. **Convert:** Use Claude Code to convert images to Markdown
5. **Learn More:** See `USAGE_GUIDE.md` for detailed examples

## File Descriptions

### Documentation Files

- **INDEX.md** (this file)
  - Overview of all files in the skill directory
  - Quick reference table
  - Getting started guide

- **README.md**
  - Main documentation
  - Feature overview
  - Installation instructions
  - Basic usage examples
  - Comparison with main library

- **USAGE_GUIDE.md**
  - Detailed workflow examples
  - Common use cases (academic papers, documentation, etc.)
  - Advanced options
  - Troubleshooting guide
  - Best practices

### Configuration Files

- **skill.json**
  - Skill metadata in JSON format
  - Command definitions
  - Dependency specifications
  - Used by skill loading systems that expect JSON

- **skill.yaml**
  - Skill metadata in YAML format
  - Same information as skill.json but in YAML
  - More human-readable
  - Includes examples and extended metadata

### Prompt Files

- **skill_main.md**
  - Main skill execution prompt
  - Complete workflow description
  - Step-by-step instructions for Claude Code
  - Error handling guidelines
  - Quality checklist

- **prompt.md**
  - Original conversion guidelines
  - Comprehensive Markdown rules
  - Element-by-element conversion guide
  - Quality standards

- **conversion_prompt.md**
  - Quick reference guide
  - Condensed conversion rules
  - Common patterns and tips
  - Easy lookup format

### Executable Files

- **pdf2md.py**
  - Standalone Python script
  - Extracts PDF pages to images
  - Self-contained (no imports from parent project)
  - Command-line interface
  - Supports page ranges, custom DPI, output directories

- **example_usage.sh**
  - Shell script with examples
  - Demonstrates common usage patterns
  - Includes test with sample PDF if available

## Workflow Overview

```
User provides PDF
    ↓
Run pdf2md.py
    ↓
Extract pages as JPG images
    ↓
Claude Code reads images
    ↓
Convert to Markdown (using prompt guidelines)
    ↓
Combine pages
    ↓
Save final Markdown file
```

## Key Features

- **No External LLM APIs**: Uses Claude Code's native vision
- **Standalone Script**: `pdf2md.py` works independently
- **Comprehensive Guides**: Multiple documentation levels
- **Flexible Configuration**: JSON or YAML metadata
- **Reference Prompts**: Multiple prompt files for different needs

## Dependencies

### Python Packages (required for pdf2md.py)
- `pymupdf` (fitz) - PDF to image conversion
- `pypdf2` - PDF page extraction

### System Requirements
- Python 3.7+
- Sufficient disk space for temporary images
- Read/write permissions for output directories

## Version Information

- **Skill Version:** 1.0.0
- **Compatible with:** Claude Code (with vision support)
- **Based on:** MarkPDFDown library v1.1.2

## License

This skill inherits the license from the parent markpdfdown project.

## Contributing

To improve this skill:
1. Test with various PDF types
2. Document edge cases in USAGE_GUIDE.md
3. Add examples to example_usage.sh
4. Refine conversion prompts based on results
5. Submit issues or pull requests

## Support

For help:
1. Check README.md for basic usage
2. Review USAGE_GUIDE.md for detailed examples
3. Test with the sample PDF: `../tests/fixtures/pdfs/input_tables.pdf`
4. Check the troubleshooting section in USAGE_GUIDE.md

## Quick Commands

```bash
# Extract PDF pages
python3 skill/pdf2md.py document.pdf --output-dir ./images

# Extract specific range
python3 skill/pdf2md.py document.pdf --start 5 --end 10 --output-dir ./images

# High resolution
python3 skill/pdf2md.py document.pdf --dpi 600 --output-dir ./images

# Get help
python3 skill/pdf2md.py --help

# Run example script
bash skill/example_usage.sh
```

---

**Last Updated:** 2026-02-14
**Maintainer:** MarkPDFDown Project
