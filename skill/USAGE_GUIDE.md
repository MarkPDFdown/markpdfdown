# PDF to Markdown Skill - Usage Guide

This guide demonstrates how to use the PDF to Markdown skill with Claude Code.

## Quick Start

### Step 1: Prepare Your Environment

Ensure you have the required dependencies installed:

```bash
pip install pymupdf pypdf2
```

### Step 2: Extract PDF Pages to Images

Use the `pdf2md.py` script to convert PDF pages to images:

```bash
python3 skill/pdf2md.py <your_pdf_file.pdf> --output-dir ./pdf_images
```

**Example:**
```bash
python3 skill/pdf2md.py research_paper.pdf --output-dir ./pdf_images --start 1 --end 10
```

This will:
- Extract pages 1-10 from `research_paper.pdf`
- Convert them to 300 DPI JPG images
- Save them to `./pdf_images/` directory
- Output: `page_0001.jpg`, `page_0002.jpg`, etc.

### Step 3: Convert Images to Markdown with Claude Code

Now you can ask Claude Code to convert each image to Markdown. Claude has vision capabilities and can read the images directly.

**Example conversation:**

```
User: I've extracted pages from my PDF to ./pdf_images/. Please convert them all to Markdown.

Claude: I'll read each image and convert it to Markdown format.

[Claude reads page_0001.jpg]

Here's the Markdown for page 1:

# Introduction to Machine Learning

Machine learning is a subset of artificial intelligence...

[Continues with remaining pages...]
```

### Step 4: Combine and Save

Claude will combine all pages into a single Markdown document and save it to your desired output file.

---

## Detailed Workflow Example

Let's walk through a complete example with a real document.

### Example: Converting a Research Paper

**Input:** `research_paper.pdf` (20 pages)

**Goal:** Convert pages 1-5 to Markdown

#### 1. Extract Pages

```bash
cd /path/to/markpdfdown-skill
python3 skill/pdf2md.py research_paper.pdf \
  --output-dir ./temp_images \
  --start 1 \
  --end 5 \
  --dpi 300
```

**Output:**
```
Successfully extracted 5 images from 20 pages
Images saved to: ./temp_images

Extracted images:
  1. ./temp_images/page_0001.jpg
  2. ./temp_images/page_0002.jpg
  3. ./temp_images/page_0003.jpg
  4. ./temp_images/page_0004.jpg
  5. ./temp_images/page_0005.jpg
```

#### 2. Review Conversion Guidelines

Before starting, review the conversion rules in `skill_main.md` or `conversion_prompt.md` to understand how Claude should format the output.

Key guidelines:
- Headings: `#`, `##`, `###` based on hierarchy
- Math: `$inline$` and `$$block$$` LaTeX format
- Tables: Markdown table syntax
- Code: ` ```language ... ``` `

#### 3. Convert Each Page

**Manual approach:**

Ask Claude Code:
```
Please read ./temp_images/page_0001.jpg and convert it to Markdown following
the guidelines in skill/conversion_prompt.md
```

Claude will analyze the image and produce Markdown output.

**Batch approach:**

Ask Claude Code:
```
Please convert all images in ./temp_images/ to Markdown. For each image:
1. Read the image
2. Convert to Markdown following skill/conversion_prompt.md
3. Save each page's Markdown
4. Combine all pages into research_paper.md with proper spacing
```

#### 4. Review and Refine

After conversion, review the output:
- Check table formatting
- Verify math formulas
- Ensure code blocks have correct language tags
- Confirm heading hierarchy

If needed, ask Claude to make corrections:
```
In research_paper.md, please fix the table on page 3 - some columns are misaligned
```

---

## Common Use Cases

### Use Case 1: Academic Papers

**Characteristics:**
- Abstract, sections, references
- Math formulas
- Tables and figures
- Citations

**Example:**
```bash
python3 skill/pdf2md.py paper.pdf --output-dir ./paper_images --dpi 300
```

**Expected Markdown structure:**
```markdown
# Title of Paper

## Abstract
...

## 1. Introduction
...

### 1.1 Background
...

## 2. Methods
...

### 2.1 Dataset
...

## References
1. Author et al. (2020)...
```

### Use Case 2: Technical Documentation

**Characteristics:**
- Code examples
- API specifications
- Tables of parameters
- Diagrams

**Example:**
```bash
python3 skill/pdf2md.py docs.pdf --start 10 --end 30 --output-dir ./docs_images
```

**Expected Markdown:**
````markdown
## API Endpoint: /users

### Request

```http
GET /api/v1/users
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | integer | Yes | User ID |
| name | string | No | User name filter |

### Response

```json
{
  "users": [...]
}
```
````

### Use Case 3: Presentation Slides

**Characteristics:**
- Each slide is a section
- Bullet points
- Images and diagrams

**Example:**
```bash
python3 skill/pdf2md.py slides.pdf --output-dir ./slides_images
```

**Expected Markdown:**
```markdown
## Slide 1: Introduction

- Topic overview
- Key objectives
- Agenda

## Slide 2: Background

- Historical context
- Current challenges
- Opportunities

...
```

### Use Case 4: Financial Reports

**Characteristics:**
- Complex tables
- Numbers and currencies
- Headers/footers
- Multi-column layouts

**Example:**
```bash
python3 skill/pdf2md.py annual_report.pdf --start 50 --end 60 --dpi 600
```

**Tips:**
- Use higher DPI (600) for better table recognition
- Pay special attention to number alignment
- May need manual review for complex financial tables

---

## Advanced Options

### Custom DPI

Adjust resolution based on content:

```bash
# Low resolution (faster, smaller files)
python3 skill/pdf2md.py doc.pdf --dpi 150

# Standard resolution (balanced)
python3 skill/pdf2md.py doc.pdf --dpi 300

# High resolution (better quality, slower)
python3 skill/pdf2md.py doc.pdf --dpi 600
```

**When to use higher DPI:**
- Small text or complex diagrams
- Tables with fine details
- Mathematical formulas with subscripts/superscripts

### Selective Page Extraction

Extract non-consecutive pages by running multiple commands:

```bash
# Extract pages 1-5
python3 skill/pdf2md.py book.pdf --start 1 --end 5 --output-dir ./chapter1

# Extract pages 20-30
python3 skill/pdf2md.py book.pdf --start 20 --end 30 --output-dir ./chapter2
```

### Custom Output Organization

Organize output by document structure:

```bash
# Introduction
python3 skill/pdf2md.py thesis.pdf --start 1 --end 10 --output-dir ./intro

# Methods
python3 skill/pdf2md.py thesis.pdf --start 11 --end 30 --output-dir ./methods

# Results
python3 skill/pdf2md.py thesis.pdf --start 31 --end 50 --output-dir ./results
```

Then ask Claude to convert each section separately.

---

## Troubleshooting

### Problem: Text is too small to read

**Solution:** Increase DPI
```bash
python3 skill/pdf2md.py doc.pdf --dpi 600
```

### Problem: Table columns are misaligned

**Solutions:**
1. Use higher DPI for better image quality
2. Ask Claude to review the table specifically
3. Manually adjust the Markdown table after conversion

### Problem: Math formulas not recognized

**Solutions:**
1. Ensure formulas are clear in the image (check DPI)
2. Ask Claude to focus on mathematical content
3. Provide examples of the LaTeX format you want

### Problem: Multi-column text is out of order

**Solution:** Claude should read left-to-right, top-to-bottom. If not:
```
Please re-read this page and maintain the reading order: left column first
(top to bottom), then right column (top to bottom)
```

### Problem: Code blocks missing language tags

**Solution:** Ask Claude to add them:
```
Please review the Markdown and add appropriate language tags to all code blocks
```

---

## Best Practices

### 1. Check Image Quality First

After extraction, quickly review 1-2 images to ensure quality:
```bash
# On Linux with image viewer
eog ./pdf_images/page_0001.jpg

# On macOS
open ./pdf_images/page_0001.jpg
```

### 2. Provide Context to Claude

When asking Claude to convert, provide context:
```
This is a research paper in computer science. Please convert the images to
Markdown, paying special attention to:
- Mathematical formulas (use LaTeX)
- Code snippets (likely Python)
- Algorithm descriptions
```

### 3. Process in Batches

For large documents, process in smaller batches:
- 5-10 pages at a time
- This makes it easier to review and catch errors
- Easier to provide specific feedback

### 4. Iterate and Refine

Don't expect perfect results on first try:
1. First pass: Get basic structure
2. Second pass: Fix tables and formulas
3. Final pass: Polish formatting and consistency

### 5. Save Intermediate Results

Save Markdown for each page separately before combining:
```
./output/
  page_01.md
  page_02.md
  page_03.md
  ...
  combined.md
```

This makes it easier to:
- Identify problematic pages
- Make targeted corrections
- Regenerate only specific pages if needed

---

## Integration with Claude Code

### Automated Workflow

You can create a simple script to automate the entire process:

```bash
#!/bin/bash
# convert_pdf.sh

PDF_FILE=$1
OUTPUT_MD=${2:-output.md}
TEMP_DIR="./temp_pdf_images"

# Extract images
echo "Extracting images from PDF..."
python3 skill/pdf2md.py "$PDF_FILE" --output-dir "$TEMP_DIR"

# Now ask Claude Code to process the images
echo "Images extracted to $TEMP_DIR"
echo "Next: Ask Claude Code to convert images to $OUTPUT_MD"
```

Usage:
```bash
./convert_pdf.sh research_paper.pdf paper.md
```

### Custom Prompts

Create custom conversion prompts for specific document types:

**For code documentation:**
```markdown
Please convert this page to Markdown:
- Code blocks should use appropriate language tags
- API endpoints should be formatted as headings
- Parameter tables should use Markdown table syntax
- Keep inline code in backticks
```

**For academic papers:**
```markdown
Please convert this page to Markdown:
- Convert all math to LaTeX (inline: $...$, block: $$...$$)
- Section numbers should be part of the heading
- Keep reference formatting consistent
- Convert figures to descriptive text with > blockquote
```

---

## Examples Gallery

See `skill/examples/` directory for:
- Sample PDFs
- Extracted images
- Converted Markdown
- Before/after comparisons

(Note: Add actual examples when available)

---

## Getting Help

If you encounter issues:

1. **Check the extraction:** Verify images are clear and readable
2. **Review guidelines:** See `skill_main.md` for conversion rules
3. **Test with sample:** Try the test PDF first: `tests/fixtures/pdfs/input_tables.pdf`
4. **Ask Claude:** Claude Code can help troubleshoot conversion issues

---

## Next Steps

After mastering basic conversion:

1. **Customize prompts** for your specific document types
2. **Create templates** for common formats
3. **Build automation scripts** for repeated tasks
4. **Contribute examples** to help others

Happy converting!
