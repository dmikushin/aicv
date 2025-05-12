"""
PDF conversion utilities for the AI-aware CV generator
"""
import os
import tempfile
import weasyprint
from pathlib import Path

def convert_html_to_pdf(html_path, pdf_path=None, paper_size="A4", add_page_numbers=True):
    """
    Convert an HTML file to PDF using WeasyPrint.

    Args:
        html_path (str): Path to the HTML file
        pdf_path (str, optional): Path for the PDF output. If None, uses the HTML path with .pdf extension
        paper_size (str, optional): Paper size for the PDF. Defaults to "A4"
        add_page_numbers (bool, optional): Whether to add page numbers. Defaults to True

    Returns:
        str: Path to the generated PDF file
    """
    if not pdf_path:
        # Use input filename with .pdf extension
        if html_path.endswith('.html'):
            pdf_path = os.path.splitext(html_path)[0] + ".pdf"
        else:
            # For temporary files with random names, use a more sensible default
            pdf_path = "cv.pdf"

    # Read the HTML content
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Add page numbers CSS if requested
    if add_page_numbers:
        # Insert page number CSS before the closing </style> tag
        page_number_css = """
        @page {
            @bottom-right {
                content: "Page " counter(page) " of " counter(pages);
                font-family: var(--font-primary);
                font-size: 10pt;
                color: #666;
                padding-right: 10mm;
            }
            size: A4 portrait;
            margin: 20mm 15mm 20mm 15mm;
        }
        """
        html_content = html_content.replace('</style>', f'{page_number_css}\n</style>')

    # Create a temporary file with the modified HTML content
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as temp_file:
        temp_file.write(html_content)
        temp_html_path = temp_file.name

    try:
        # Convert HTML to PDF
        html = weasyprint.HTML(filename=temp_html_path)
        pdf = html.write_pdf()

        # Write the PDF to file
        with open(pdf_path, 'wb') as f:
            f.write(pdf)

        print(f"PDF saved to {pdf_path}")
        return pdf_path

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_html_path):
            os.unlink(temp_html_path)
