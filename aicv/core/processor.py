"""
Core logic for the AI-aware CV generator
"""
from typing import Dict, Any, Optional
from aicv.core.extensions import PyMdExtension, PyMdPreprocessor
from aicv.backend.markdown import create_markdown
from aicv.backend.html import create_html
from aicv.backend.moderncv import create_moderncv

def generate(file_path: str, personal_info: Dict[str, Any], backend: str = 'markdown', emojis: bool = True) -> str:
    """Reads a Markdown file, processes it with the custom extension, and returns the
    processed markdown, html or latex content.
    This provides a clean intermediate markdown, html or latex representation.

    Args:
        file_path (str): Path to the Markdown file
        personal_info (Dict[str, Any]): Personal information dictionary
        backend (str): The backend to use for processing. Can be 'markdown', 'html', or 'moderncv'
        emojis (bool): Whether to enable emojis in the CV text (except personal info)
    Returns:
        str: The processed content with all pymd blocks executed
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

    preprocessor = PyMdPreprocessor(personal_info, backend=backend, emojis=emojis)
    processed_lines = preprocessor.run(file_content.splitlines())
    processed_content = '\n'.join(processed_lines)

    if backend == 'html':
        return create_html(processed_content, personal_info, emojis=emojis)
    elif backend == 'moderncv':
        # Pass the bibliography content collected during processing
        bib_content = getattr(preprocessor, 'bib_content', '')
        return create_moderncv(processed_content, personal_info, bib_content)
    else: # markdown
        return create_markdown(processed_content, personal_info, emojis=emojis)
