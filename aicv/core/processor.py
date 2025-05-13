"""
Core markdown processing logic for the AI-aware CV generator
"""
import markdown
from pathlib import Path
import base64
from aicv.core.extensions import PyMdExtension, PyMdPreprocessor
from aicv.utils.text_processing import convert_markdown_links, add_section_emojis
from aicv.utils.html_generator import create_styled_html
import sys
import os
import json

def generate(file_path, personal_info, backend='markdown', emojis=True):
    """Reads a Markdown file, processes it with the custom extension, and returns the
    processed markdown or html content.
    This provides a clean intermediate markdown or html representation.
    
    Args:
        file_path (str): Path to the Markdown file
        personal_info (dict): Personal information dictionary
        backend (str): The backend to use for processing. Can be 'markdown' or 'html'
        emojis (bool): Whether to enable emojis in the CV text (except personal info)
    Returns:
        str: The processed content with all pymd blocks executed
    """
    with open(file_path, 'r') as f:
        file_content = f.read()

    preprocessor = PyMdPreprocessor(personal_info, backend=backend, emojis=emojis)
    processed_lines = preprocessor.run(file_content.splitlines())
    processed_content = '\n'.join(processed_lines)

    if backend == 'html':
        return create_styled_html(processed_content, personal_info, emojis=emojis)
    else:
        # Import here to avoid circular imports
        from aicv.utils.text_processing import format_personal_info
        
        # Format personal info fields with proper formatting
        info_lines = [
            f"- **Name**: {format_personal_info(personal_info, 'name', 'markdown')}",
            f"- **Position**: {format_personal_info(personal_info, 'position', 'markdown')}",
            f"- **Address**: {format_personal_info(personal_info, 'address', 'markdown')}",
            f"- **Phone**: {format_personal_info(personal_info, 'phone', 'markdown')}",
            f"- **Email**: {format_personal_info(personal_info, 'email', 'markdown')}",
            f"- **Website**: {format_personal_info(personal_info, 'website', 'markdown')}",
            f"- **GitHub**: {format_personal_info(personal_info, 'github', 'markdown')}",
            f"- **Date of Birth**: {format_personal_info(personal_info, 'date_of_birth', 'markdown')}"
        ]
        return '\n'.join(info_lines) + '\n\n' + processed_content


def process_markdown_to_html(markdown_content, personal_info, photo_html):
    """Processes markdown content into HTML.
    This is the second stage of the pipeline, taking the output from generate_markdown().
    
    Args:
        markdown_content (str): The processed markdown content
        photo_html (str): HTML for the photo section
        personal_info (dict, optional): Personal information dictionary. If None, will be extracted from markdown.
        
    Returns:
        str: The processed HTML content
    """
    # Convert processed markdown to HTML
    md = markdown.Markdown(extensions=[PyMdExtension()])
    html_content = md.convert(markdown_content)

    # Process the content to add section emojis and convert markdown links
    content = convert_markdown_links(html_content)
    content = add_section_emojis(content)

    # Create the final HTML document
    html_document = create_styled_html(content, personal_info, photo_html)

    return html_document
