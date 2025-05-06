#!/usr/bin/env python3
"""
Test script for HTML rendering in AICV.
This script checks if the HTML renderer correctly generates expected HTML fragments.
"""
import os
import sys
import argparse
import re
from pathlib import Path

# Add parent directory to path to import aicv modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from aicv.utils.html_generator import create_styled_html
from aicv.core.processor import process_markdown_to_html

def load_html_fragments(fragments_dir):
    """Load all HTML fragments from the specified directory."""
    fragments = {}
    for filename in os.listdir(fragments_dir):
        if filename.endswith('.html'):
            fragment_path = os.path.join(fragments_dir, filename)
            fragment_name = os.path.splitext(filename)[0]
            with open(fragment_path, 'r', encoding='utf-8') as f:
                fragments[fragment_name] = f.read().strip()
    return fragments

def normalize_html(html):
    """Normalize HTML by removing extra whitespace and standardizing tags."""
    # Replace multiple whitespace with single space
    html = re.sub(r'\s+', ' ', html)
    # Trim space around tags
    html = re.sub(r'\s*>\s*', '>', html)
    html = re.sub(r'\s*<\s*', '<', html)
    return html.strip()

def test_html_rendering(cv_path, fragments_dir):
    """Test if the HTML rendering contains the expected fragments."""
    
    # Create dummy personal info for testing
    personal_info = {
        'name': 'John Doe',
        'position': 'Software Engineer',
        'address': 'New York, USA',
        'phone': '+1 555-123-4567',
        'email': 'john.doe@example.com',
        'website': 'example.com',
        'github': 'johndoe',
        'date_of_birth': 'January 1, 1980'
    }
    
    # 1. Load test HTML fragments
    fragments = load_html_fragments(fragments_dir)
    if not fragments:
        print("Error: No HTML fragments found.")
        return False
    
    # 2. If cv_path is provided, use its content, otherwise use example text
    if cv_path and os.path.exists(cv_path):
        with open(cv_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
    else:
        md_content = """
# John Doe

## 💼 Professional Experience

### 🚀 Co-Founder & CTO at Purple Gaze Inc.
*December 2019 - Present*

- **Location:** Lausanne Area, Switzerland
- **Responsibilities:**
  - Developed research-quality high-performance eyetracking hardware and software stack

## 🎓 Education

### 📝 Doctor of Philosophy (PhD) in Business Analytics
*May 2019 - February 2023*

- **Institution:** University of Lausanne (UNIL)
- **Location:** Lausanne, Switzerland
- **Dissertation:** High-performance computing approaches to solve large-scale dynamic models

## 📚 Publications (peer-reviewed)

- 🔥 Nishikawa, H., Nakashima, Y., Doe, J., & Lee, J. (2025). A Reduced-Memory Multicolor Gauss-Seidel Relaxation Scheme for Implicit Unstructured-Polyhedral-Grid CFD Solver on GPU. In *AIAA AVIATION 2025 Forum*. (to appear).
"""

    # Process markdown and generate HTML
    photo_html = ""  # Empty photo for testing
    html_output = process_markdown_to_html(md_content, photo_html)  # Generate HTML
    
    # Save the generated HTML to a file for inspection
    debug_output_path = os.path.join(os.path.dirname(fragments_dir), "debug_output.html")
    with open(debug_output_path, 'w', encoding='utf-8') as f:
        f.write(html_output)
    print(f"Debug output saved to {debug_output_path}")
    
    # Normalize HTML output for comparison
    normalized_output = normalize_html(html_output)
    
    # 3. Check if all fragments are present in the HTML output
    failures = []
    for name, fragment in fragments.items():
        # Normalize fragment for comparison
        normalized_fragment = normalize_html(fragment)
        
        if normalized_fragment in normalized_output:
            print(f"✅ Fragment '{name}' found in HTML output")
        else:
            failures.append(name)
            print(f"❌ Fragment '{name}' not found in HTML output")
            
            # Provide diagnostic information
            print(f"  Fragment content: {normalized_fragment}")
            # Try to find partial matches to help diagnose issues
            for line in normalized_fragment.split('>'):
                if line and line + '>' in normalized_output:
                    print(f"  Partial match found for: {line}> ✓")
                elif line:
                    print(f"  No match for: {line}> ✗")
    
    # Report results
    if failures:
        print(f"\nTest failed: {len(failures)} of {len(fragments)} fragments not found in HTML output")
        return False
    else:
        print(f"\nTest passed: All {len(fragments)} fragments found in HTML output")
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test HTML rendering")
    parser.add_argument("--cv", help="Path to Markdown CV file to test")
    args = parser.parse_args()
    
    fragments_dir = os.path.join(os.path.dirname(__file__), "fragments")
    success = test_html_rendering(args.cv, fragments_dir)
    
    sys.exit(0 if success else 1)