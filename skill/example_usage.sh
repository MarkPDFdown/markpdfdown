#!/bin/bash
# Example usage of the PDF to Markdown skill

echo "=== PDF to Markdown Skill - Example Usage ==="
echo ""

# Example 1: Basic usage
echo "Example 1: Extract images from a PDF"
echo "Command: python3 pdf2md.py input.pdf"
echo ""

# Example 2: With page range
echo "Example 2: Extract specific pages"
echo "Command: python3 pdf2md.py document.pdf --start 1 --end 10"
echo ""

# Example 3: Custom output directory
echo "Example 3: Custom output directory"
echo "Command: python3 pdf2md.py report.pdf --output-dir ./my_images"
echo ""

# Example 4: High resolution
echo "Example 4: High resolution extraction"
echo "Command: python3 pdf2md.py slides.pdf --dpi 600"
echo ""

# Example 5: Full options
echo "Example 5: All options"
echo "Command: python3 pdf2md.py book.pdf --output-dir ./chapters --start 5 --end 20 --dpi 300"
echo ""

echo "=== Testing with Sample PDF ==="
echo ""

# Check if sample PDF exists
if [ -f "../tests/fixtures/pdfs/input_tables.pdf" ]; then
    echo "Found sample PDF: tests/fixtures/pdfs/input_tables.pdf"
    echo "Running extraction..."
    echo ""

    python3 pdf2md.py ../tests/fixtures/pdfs/input_tables.pdf --output-dir ./test_output

    echo ""
    echo "Check ./test_output for extracted images"
else
    echo "Sample PDF not found. Please provide your own PDF file."
    echo "Usage: python3 pdf2md.py <your_pdf_file.pdf>"
fi

echo ""
echo "=== Next Steps ==="
echo "1. Review the extracted images in the output directory"
echo "2. Use Claude Code to convert each image to Markdown"
echo "3. Combine all Markdown pages into a single document"
echo ""
