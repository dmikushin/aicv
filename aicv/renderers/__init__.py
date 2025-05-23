"""
Renderers package for the AI-aware CV generator
"""
import json
import os
from .education import render_education
from .employment import render_employment
from .publications import render_publications

def render(json_filename, backend, emojis=True):
    """Reads a JSON file and renders the content based on its type and backend."""
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
        result = render_education(data["education"], backend, emojis=emojis)
        print(result)
        return result
    elif "employment" in data:
        result = render_employment(data["employment"], backend, emojis=emojis)
        print(result)
        return result
    elif "publications" in data:
        result = render_publications(data["publications"], backend, emojis=emojis)

        # Handle moderncv publications which return tuple (latex_content, bib_content)
        if backend == 'moderncv' and isinstance(result, tuple) and len(result) == 2:
            latex_content, bib_content = result
            print(latex_content)
            return result  # Return the tuple for processing in extensions
        else:
            print(result)
            return result
    else:
        print("Invalid data format.")
        return None
