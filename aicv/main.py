#!/usr/bin/env python3
"""
AI-aware Curriculum Vitae Generator
Main entry point for the CV generation tool
"""

import argparse
import json
import os
from aicv.core.processor import generate # Keep this for other backends
from aicv.utils.pdf_converter import convert_html_to_pdf
from aicv.utils.latex_compiler import compile_latex_to_pdf

def main():
    """Main entry point for the CV generation tool"""
    parser = argparse.ArgumentParser(description='Process a Markdown file with pymd blocks.')
    parser.add_argument('file_path', type=str, help='Path to the Markdown file (used as a base for finding JSON data)')
    parser.add_argument('--output', '-o', type=str, help='Output HTML file path (default: input_file.html)')
    parser.add_argument('--pdf', '-p', action='store_true', help='Generate PDF output only (no HTML via WeasyPrint)')
    parser.add_argument('--pdf-output', type=str, help='Output PDF file path (default: input_file.pdf)')
    parser.add_argument('--moderncv', action='store_true', help='Generate PDF output using moderncv LaTeX style')
    # The --bibtex flag for compile_latex_to_pdf is handled by checking if a .bib file was generated.
    # No explicit user flag needed if we auto-detect based on bib_content.
    parser.add_argument('--paper', type=str, default='A4', help='PDF paper size (default: A4, for WeasyPrint PDF)')
    parser.add_argument('--no-page-numbers', action='store_true', help='Disable page numbers in PDF output (for WeasyPrint PDF)')
    parser.add_argument('--markdown', type=str, help='Output intermediate Markdown file and exit')
    parser.add_argument('--emojis', dest='emojis', action='store_true', help='Enable emojis in CV text (except personal info and LaTeX)')
    parser.add_argument('--no-emojis', dest='emojis', action='store_false', help='Disable emojis in CV text')
    parser.set_defaults(emojis=None)
    args = parser.parse_args()

    input_dir = os.path.dirname(os.path.abspath(args.file_path))
    personal_json_path = os.path.join(input_dir, 'personal.json')
    with open(personal_json_path, 'r') as personal_file:
        personal_info = json.load(personal_file)

    if 'photo' in personal_info and personal_info['photo']:
        photo_path = personal_info['photo']
        if not os.path.isabs(photo_path):
            personal_info['photo_path'] = os.path.abspath(os.path.join(input_dir, photo_path))
        else:
            personal_info['photo_path'] = photo_path
    else:
        personal_info['photo_path'] = None

    if args.markdown:
        backend = 'markdown'
    elif args.moderncv:
        backend = 'moderncv'
    else:
        backend = 'html'

    if args.emojis is None:
        if backend == 'markdown' or backend == 'moderncv':
            emojis_enabled = False
        else: # html
            emojis_enabled = True
    else:
        emojis_enabled = args.emojis

    # For moderncv, emojis are typically not used. Override if backend is moderncv.
    if backend == 'moderncv':
        emojis_enabled = False

    bib_content = "" # Initialize bib_content for moderncv case
    content = generate(args.file_path, personal_info, backend=backend, emojis=emojis_enabled)

    if args.markdown:
        with open(args.markdown, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Markdown representation saved to {args.markdown}")
        return

    output_pdf_path = args.pdf_output
    if not output_pdf_path:
        base, _ = os.path.splitext(args.file_path)
        output_pdf_path = base + ".pdf"

    if args.moderncv:
        # 'content' here is latex_content
        tex_base_name = os.path.splitext(output_pdf_path)[0]
        tex_path = tex_base_name + ".tex"
        bib_path = tex_base_name + ".bib"

        with open(tex_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Intermediate LaTeX file saved to {tex_path}")

        # TODO Embed inlined BibTeX into .tex file itself, this is possible
        use_bibtex_run = False
        if bib_content: # bib_content
            with open(bib_path, 'w', encoding='utf-8') as f_bib:
                f_bib.write(bib_content)
            print(f"BibTeX file saved to {bib_path}")
            use_bibtex_run = True

        # Pass the directory of the tex file as current_working_dir
        # and the bibtex flag to the compiler function.
        # The personal_info argument is removed from compile_latex_to_pdf
        compile_latex_to_pdf(tex_path, output_pdf_path, use_bibtex=use_bibtex_run, working_directory=os.path.dirname(tex_path))

    elif args.pdf: # PDF via HTML (WeasyPrint)
        try:
            html_content_for_pdf = content
            if backend != 'html': # If user specified --pdf with --markdown (which exits) or an unexpected state
                # This case should ideally not be hit if --markdown exits.
                # If we are here, it means --pdf is true, --moderncv is false.
                # We need HTML content.
                print(f"Warning: Generating PDF from a non-HTML backend ('{backend}'). Re-generating content as HTML.")
                html_content_for_pdf = generate(args.file_path, personal_info, backend='html', emojis=emojis_enabled)

            # Determine path for the HTML file to be converted
            # If args.output (HTML output path) is specified, use it. Otherwise, create a temporary HTML file.
            html_to_convert_path = args.output
            created_temp_html = False
            if not html_to_convert_path:
                # Create a temporary HTML file path
                temp_html_dir = os.path.dirname(output_pdf_path) # Save temp HTML near PDF
                temp_html_name = os.path.splitext(os.path.basename(output_pdf_path))[0] + "_temp_for_pdf.html"
                html_to_convert_path = os.path.join(temp_html_dir, temp_html_name)
                created_temp_html = True

            # Write the HTML content to the path (either user-specified or temporary)
            # The 'generate' function for HTML backend already produces a full HTML document string.
            with open(html_to_convert_path, 'w', encoding='utf-8') as f:
                 f.write(html_content_for_pdf)
            if created_temp_html:
                print(f"Temporary HTML for PDF generation saved to {html_to_convert_path}")

            convert_html_to_pdf(html_to_convert_path, output_pdf_path, paper_size=args.paper, add_page_numbers=not args.no_page_numbers)

            if created_temp_html and os.path.exists(html_to_convert_path): # Clean up temp html
                os.remove(html_to_convert_path)
                print(f"Removed temporary HTML file: {html_to_convert_path}")

        except ImportError:
            print("WeasyPrint is not installed. Please install it to generate PDF output from HTML.")
            print("You can install it with: pip install weasyprint")
        except Exception as e:
            print(f"An error occurred during PDF generation via HTML: {e}")

    elif not args.pdf and not args.moderncv: # Only generate HTML
        output_html_path = args.output or os.path.splitext(args.file_path)[0] + ".html"
        # 'content' is already the full HTML string from generate()
        with open(output_html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"HTML output saved to {output_html_path}")

if __name__ == "__main__":
    main()
