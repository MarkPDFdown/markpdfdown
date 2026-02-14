# PDF to Markdown Conversion Skill

You are executing the PDF to Markdown conversion skill. Your task is to convert a PDF document into well-formatted Markdown.

## Workflow

Follow these steps to convert a PDF to Markdown:

### Step 1: Extract PDF Information

First, use the PDF extraction script to convert PDF pages into images:

```bash
python3 skill/pdf2md.py <input_pdf> --output-dir <temp_dir> [--start <start_page>] [--end <end_page>] [--dpi <dpi>]
```

This will:
- Extract pages from the PDF as high-resolution images
- Save them to the specified output directory
- Print the list of extracted image files

### Step 2: Process Each Page Image

For each extracted image, you need to:

1. **Read the image** using the Read tool to view its content
2. **Analyze the content** and convert it to Markdown following the conversion guidelines
3. **Save the Markdown** for this page

### Step 3: Combine All Pages

After processing all pages:
1. Combine all page Markdown into a single document
2. Add appropriate spacing between pages (use `\n\n` between pages)
3. Ensure consistent formatting throughout

### Step 4: Save Final Output

Write the complete Markdown to the output file specified by the user (or `<input_name>.md` by default).

## Conversion Guidelines

When converting each page image to Markdown, follow these rules:

### Document Structure

- **Headings**: Use `#`, `##`, `###` etc. based on visual hierarchy
  - Main title: `# Title`
  - Sections: `## Section`
  - Subsections: `### Subsection`

- **Paragraphs**: Separate with blank lines

- **Lists**:
  - Unordered: `- item` or `* item`
  - Ordered: `1. item`, `2. item`
  - Nested: indent with 2-4 spaces

### Text Formatting

- **Bold**: `**text**`
- **Italic**: `*text*`
- **Code**: `` `code` ``
- **Links**: `[text](url)` when URLs are visible

### Tables

Format as Markdown tables:
```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
```

- Align columns properly
- Preserve all table content
- Use appropriate cell separators

### Mathematical Formulas

- **Inline math**: `$formula$`
  - Example: `$E = mc^2$`

- **Block math**: `$$formula$$`
  - Example:
    ```
    $$
    \int_{a}^{b} f(x) dx = F(b) - F(a)
    $$
    ```

- Use proper LaTeX syntax
- Preserve all mathematical notation accurately

### Code Blocks

````markdown
```language
code here
```
````

- Specify programming language when identifiable
- Preserve indentation and formatting
- Common languages: python, javascript, java, cpp, etc.

### Images and Diagrams

- **Photos/Images**: `![Description](url_if_available)`
- **Diagrams/Charts**: Provide descriptive text
  ```markdown
  > **Figure N**: Detailed description of the diagram, chart, or illustration
  ```

### Special Elements

- **Headers/Footers**: Include only if they contain important information
- **Page Numbers**: Omit unless contextually important
- **Watermarks**: Ignore
- **Multi-column Text**: Convert to single column, maintain reading order (left-to-right, top-to-bottom)
- **Footnotes**: Use `[^1]` notation:
  ```markdown
  Text with footnote[^1]

  [^1]: Footnote content here
  ```

## Output Requirements

- **Clean Markdown**: Output only the Markdown content, no meta-comments
- **No Code Block Wrappers**: Don't wrap the entire output in ````markdown` blocks
- **Proper Spacing**: Use blank lines between sections, paragraphs, and elements
- **Accuracy**: Ensure all text is captured accurately
- **Completeness**: Don't omit content unless it's purely decorative

## Quality Checklist

Before finalizing each page:
- [ ] All text has been captured
- [ ] Headings use appropriate levels
- [ ] Tables are properly formatted
- [ ] Math formulas use correct LaTeX syntax
- [ ] Code blocks specify language
- [ ] Lists are properly formatted
- [ ] Document structure is logical and readable

## Example Usage

If the user runs:
```
/pdf2md research_paper.pdf --start 1 --end 5
```

You should:
1. Run: `python3 skill/pdf2md.py research_paper.pdf --output-dir ./temp_pdf_images --start 1 --end 5`
2. Read each generated image (page_0001.jpg, page_0002.jpg, etc.)
3. Convert each image to Markdown
4. Combine all pages with `\n\n` separators
5. Save to `research_paper.md`
6. Clean up temporary images (optional)

## Error Handling

If you encounter errors:
- **PDF not found**: Verify the file path and inform the user
- **Invalid page range**: Check that start/end pages are valid
- **Image read errors**: Ensure images were extracted successfully
- **Conversion issues**: Ask the user for clarification if content is unclear

## Notes

- This skill leverages your native vision capabilities to read PDF page images
- No external LLM API is used - you perform all analysis directly
- The PDF extraction script (`pdf2md.py`) reuses the existing `file_worker.py` from the markpdfdown library
- Focus on accuracy and maintaining document structure

Begin the conversion process when the user invokes this skill!
