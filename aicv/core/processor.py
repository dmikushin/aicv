"""
Core markdown processing logic for the AI-aware CV generator
"""
import markdown
from pathlib import Path
import base64
from aicv.core.extensions import PyMdExtension
from aicv.utils.text_processing import remove_personal_info_items, extract_personal_info, convert_markdown_links, add_section_emojis
from aicv.utils.html_generator import create_styled_html
import sys
import os

def process_markdown(file_path):
    """Reads a Markdown file, processes it with the custom extension, and returns the processed content.
    """
    with open(file_path, 'r') as f:
        text = f.read()

    # Remove personal information items that will be in the header
    text_without_personal = remove_personal_info_items(text)

    md = markdown.Markdown(extensions=[PyMdExtension()])
    html_content = md.convert(text_without_personal)

    # Extract personal information from the original markdown text
    personal_info = extract_personal_info(text)

    # Process the content to add section emojis and convert markdown links
    content = convert_markdown_links(html_content)
    content = add_section_emojis(content)

    # Check if the person has a photo
    photo_html = get_photo_html(file_path, personal_info['name'])

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
