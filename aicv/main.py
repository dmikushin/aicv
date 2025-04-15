#!/usr/bin/env python3
"""
AI-aware Curriculum Vitae Generator
Main entry point for the CV generation tool
"""

import argparse
import os
from aicv.core.processor import process_markdown
from aicv.utils.html_generator import create_html_file

def main():
    """Main entry point for the CV generation tool"""
    parser = argparse.ArgumentParser(description='Process a Markdown file with pymd blocks.')
    parser.add_argument('file_path', type=str, help='Path to the Markdown file')
    parser.add_argument('--output', '-o', type=str, help='Output HTML file path (default: input_file.html)')
    args = parser.parse_args()

    # Process the markdown file
    html_content = process_markdown(args.file_path)

    # Determine output path
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
