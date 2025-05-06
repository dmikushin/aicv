#!/usr/bin/env python3
"""
Helper script to generate example HTML from CV markdown
"""
import os
import sys
from pathlib import Path

# Add parent directory to path to import aicv modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from aicv.core.processor import process_markdown_to_html

def main():
    # Get example CV path
    example_cv_path = os.path.join(Path(__file__).parent.parent, "example", "cv.md")
    output_path = os.path.join(Path(__file__).parent, "example_rendered.html")
    
    # Read the example CV markdown
    with open(example_cv_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Generate HTML
    html_output = process_markdown_to_html(md_content, "")
    
    # Write HTML to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_output)
    
    print(f"Example HTML saved to {output_path}")

if __name__ == "__main__":
    main()