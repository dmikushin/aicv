"""
Core markdown processing logic for the AI-aware CV generator
"""
import markdown
from pathlib import Path
import base64
from aicv.core.extensions import PyMdExtension, PyMdPreprocessor
from aicv.utils.text_processing import remove_personal_info_items, extract_personal_info, convert_markdown_links, add_section_emojis
from aicv.utils.html_generator import create_styled_html
import sys
import os

def generate_markdown(file_path):
    """Reads a Markdown file, processes it with the custom extension, and returns the processed markdown content.
    This provides a clean intermediate markdown representation before HTML conversion.
    
    Args:
        file_path (str): Path to the Markdown file
        
    Returns:
        str: The processed markdown content with all pymd blocks executed
    """
    with open(file_path, 'r') as f:
        text = f.read()

    # Create a PyMdPreprocessor instance
    preprocessor = PyMdPreprocessor(markdown.Markdown())
    
    # Run the preprocessor on the file content - this executes pymd blocks
    # and replaces them with their output
    processed_lines = preprocessor.run(text.splitlines())
    
    # Join the lines back together
    processed_markdown = '\n'.join(processed_lines)
    
    return processed_markdown

def process_markdown_to_html(markdown_content, photo_html):
    """Processes markdown content into HTML.
    This is the second stage of the pipeline, taking the output from generate_markdown().
    
    Args:
        markdown_content (str): The processed markdown content
        photo_html (str): HTML for the photo section
        
    Returns:
        str: The processed HTML content
    """
    # Extract personal information from the processed markdown
    personal_info = extract_personal_info(markdown_content)

    # Remove personal information items that will be in the header
    text_without_personal = remove_personal_info_items(markdown_content)

    # Convert processed markdown to HTML
    md = markdown.Markdown(extensions=[PyMdExtension()])
    html_content = md.convert(text_without_personal)

    # Process the content to add section emojis and convert markdown links
    content = convert_markdown_links(html_content)
    content = add_section_emojis(content)

    # Create the final HTML document
    html_document = create_styled_html(content, personal_info, photo_html)

    return html_document

def get_photo_html(file_path, name):
    """Generates the HTML for the photo section"""
    # Look for photo.jpg in the same directory as the CV file
    photo_data = ""
    photo_path = Path(file_path).parent / "photo.jpg"
    photo_html = '<div class="photo-placeholder">120 × 150</div>'

    try:
        if photo_path.exists():
            with open(photo_path, "rb") as img_file:
                photo_bytes = img_file.read()
                photo_base64 = base64.b64encode(photo_bytes).decode('utf-8')
                photo_data = f"data:image/jpeg;base64,{photo_base64}"
                photo_html = f'<img src="{photo_data}" alt="{name}" style="width: 100%; height: 100%; object-fit: cover;">'
                print(f"Photo found and embedded: {photo_path}")
    except Exception as e:
        print(f"Error processing photo: {e}")

    return photo_html