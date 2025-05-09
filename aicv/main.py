#!/usr/bin/env python3
"""
AI-aware Curriculum Vitae Generator
Main entry point for the CV generation tool
"""

import argparse
import os
import tempfile
from aicv.core.processor import generate_markdown, process_markdown_to_html, get_photo_html
from aicv.utils.text_processing import extract_personal_info
from aicv.utils.html_generator import create_html_file

def main():
    """Main entry point for the CV generation tool"""
    parser = argparse.ArgumentParser(description='Process a Markdown file with pymd blocks.')
    parser.add_argument('file_path', type=str, help='Path to the Markdown file')
    parser.add_argument('--output', '-o', type=str, help='Output HTML file path (default: input_file.html)')
    parser.add_argument('--pdf', '-p', action='store_true', help='Generate PDF output only (no HTML)')
    parser.add_argument('--pdf-output', type=str, help='Output PDF file path (default: input_file.pdf)')
    parser.add_argument('--paper', type=str, default='A4', help='PDF paper size (default: A4)')
    parser.add_argument('--no-page-numbers', action='store_true', help='Disable page numbers in PDF output')
    parser.add_argument('--markdown', type=str, help='Output intermediate Markdown file and exit')
    args = parser.parse_args()

    # First stage of pipeline: Generate the intermediate markdown representation
    markdown_content = generate_markdown(args.file_path)
    
    # If markdown output is requested, save it and exit
    if args.markdown:
        # Write to the specified file
        with open(args.markdown, 'w') as f:
            f.write(markdown_content)
        
        print(f"Markdown representation saved to {args.markdown}")
        return  # Exit early, don't generate HTML/PDF

    # Extract personal information for the photo
    personal_info = extract_personal_info(markdown_content)
    
    # Get the photo HTML
    photo_html = get_photo_html(args.file_path, personal_info['name'])
    
    # Second stage of pipeline: Convert markdown to HTML
    html_content = process_markdown_to_html(markdown_content, photo_html)

    # Determine if we should generate HTML or PDF
    if args.pdf:
        try:
            from aicv.utils.pdf_converter import convert_html_to_pdf

            # Determine PDF output path
            if args.pdf_output:
                pdf_path = args.pdf_output
            else:
                # Use input filename with .pdf extension
                base_name = os.path.splitext(args.file_path)[0]
                pdf_path = f"{base_name}.pdf"

            # Create a temporary HTML file for PDF conversion
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp_file:
                temp_html_path = temp_file.name
                create_html_file(html_content, temp_html_path, silent=True)

            try:
                # Convert HTML to PDF
                convert_html_to_pdf(
                    html_path=temp_html_path,
                    pdf_path=pdf_path,
                    paper_size=args.paper,
                    add_page_numbers=not args.no_page_numbers
                )
            finally:
                # Clean up temporary HTML file
                if os.path.exists(temp_html_path):
                    os.unlink(temp_html_path)

        except ImportError:
            print("Error: WeasyPrint is required for PDF generation.")
            print("Please install it with: pip install weasyprint")
    else:
        # Only generate HTML if --pdf is not specified
        # Determine output path for HTML
        if args.output:
            output_path = args.output
        else:
            # Use input filename with .html extension
            base_name = os.path.splitext(args.file_path)[0]
            output_path = f"{base_name}.html"

        # Create the HTML file
        create_html_file(html_content, output_path)

if __name__ == "__main__":
    main()