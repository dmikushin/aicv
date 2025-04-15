"""
Renderers package for the AI-aware CV generator
"""
import json
import os
from .education import render_education
from .employment import render_employment
from .publications import render_publications

def render(json_filename):
    """Reads a JSON file and renders the content based on its type."""
    # Check if the file exists in the current directory
    if not os.path.exists(json_filename):
        # If not, check in the same directory as cv.md
        cv_md_path = os.path.join(os.path.dirname(__file__), '../../example/cv.md')
        json_filename = os.path.join(os.path.dirname(cv_md_path), os.path.basename(json_filename))

    if not os.path.exists(json_filename):
        print(f"File {json_filename} not found.")
        return

    with open(json_filename, 'r') as f:
        data = json.load(f)

    if "education" in data:
        print(render_education(data["education"]))
    elif "employment" in data:
        print(render_employment(data["employment"]))
    elif "publications" in data:
        print(render_publications(data["publications"]))
    else:
        print("Invalid data format.")
