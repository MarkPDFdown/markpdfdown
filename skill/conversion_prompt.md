# Quick Markdown Conversion Reference

This is a condensed reference for converting PDF page images to Markdown.

## Structure Elements

| Element | Markdown Syntax | Example |
|---------|----------------|---------|
| Title | `# Title` | `# Introduction to AI` |
| Section | `## Section` | `## Background` |
| Subsection | `### Subsection` | `### Related Work` |
| Paragraph | Text with blank lines | Regular paragraph text |
| Bold | `**text**` | `**important**` |
| Italic | `*text*` | `*emphasis*` |
| Code | `` `code` `` | `` `function()` `` |
| Link | `[text](url)` | `[Google](https://google.com)` |

## Lists

**Unordered:**
```markdown
- First item
- Second item
  - Nested item
  - Another nested
```

**Ordered:**
```markdown
1. First step
2. Second step
   1. Sub-step
   2. Another sub-step
```

## Tables

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |
```

## Math

**Inline:** `$E = mc^2$`

**Block:**
```
$$
\sum_{i=1}^{n} x_i = x_1 + x_2 + \cdots + x_n
$$
```

## Code Blocks

````markdown
```python
def hello():
    print("Hello!")
```
````

## Images & Figures

```markdown
![Image description](url)

> **Figure 1**: Description of diagram or chart
```

## Footnotes

```markdown
Some text with a footnote[^1]

[^1]: The footnote content
```

## Common Patterns

### Research Papers
- Title: `#`
- Abstract: `## Abstract`
- Sections: `##` (Introduction, Methods, Results, etc.)
- References: `## References` with numbered list

### Technical Documentation
- Use code blocks for commands/code
- Tables for specifications
- Nested lists for procedures

### Presentations/Slides
- Each slide title: `##`
- Bullet points: `-` or `1.`
- Keep formatting simple

## Tips

1. **Accuracy First**: Get the text right before worrying about perfect formatting
2. **Preserve Structure**: Maintain the document's logical hierarchy
3. **Clean Output**: No explanations, just pure Markdown
4. **Consistent Style**: Use the same patterns throughout
5. **Test Math**: Ensure LaTeX formulas are valid

## What to Skip

- Page numbers (unless important)
- Headers/footers (unless important)
- Watermarks
- Purely decorative elements
- Redundant spacing/formatting

## Multi-Column Handling

For multi-column layouts:
1. Read left column top to bottom
2. Then right column top to bottom
3. Combine in reading order
4. Maintain paragraph breaks

## Quality Checks

- [ ] All visible text captured
- [ ] Headings properly leveled
- [ ] Tables formatted correctly
- [ ] Math in LaTeX
- [ ] Code blocks have language tags
- [ ] Links preserved
- [ ] Structure is logical
