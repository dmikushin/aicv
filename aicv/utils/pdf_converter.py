"""
Enhanced PDF conversion utilities for the AI-aware CV generator with ATS support
"""
import os
import json
import tempfile
import weasyprint
from pathlib import Path


def create_ats_json_overlay(employment_data, education_data, publications_data):
    """Create invisible but selectable JSON overlay for ATS parsing."""
    
    # Create structured JSON data
    ats_data = {
        "employment": employment_data,
        "education": education_data,
        "publications": publications_data
    }
    
    # Format as readable JSON
    json_content = json.dumps(ats_data, indent=2, ensure_ascii=False)
    
    # Create invisible HTML overlay
    overlay_html = f'''
    <div style="position: absolute; left: -9999px; color: transparent; font-size: 1px; 
                line-height: 1px; z-index: 1000; user-select: text; 
                -webkit-user-select: text; -moz-user-select: text; -ms-user-select: text;">
        <div id="ats-structured-data">
            ATS_DATA_START
            {json_content}
            ATS_DATA_END
        </div>
    </div>
    '''
    
    return overlay_html


def modify_html_for_ats_compatibility(html_content, employment_data=None, 
                                     education_data=None, publications_data=None):
    """
    Modify HTML content to be ATS-compatible by making visible text non-selectable
    and adding invisible structured JSON data.
    """
    
    # ATS-specific CSS
    ats_css = '''
    <style>
    /* ATS Compatibility Styles */
    .cv-content {
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        -webkit-touch-callout: none;
        -webkit-tap-highlight-color: transparent;
    }
    
    .ats-overlay {
        position: absolute;
        left: -9999px;
        top: 0;
        color: transparent;
        font-size: 1px;
        line-height: 1px;
        z-index: 1000;
        user-select: text !important;
        -webkit-user-select: text !important;
        -moz-user-select: text !important;
        -ms-user-select: text !important;
        white-space: pre-wrap;
        font-family: monospace;
        overflow: hidden;
        width: 1px;
        height: 1px;
    }
    
    /* Ensure all ATS data elements are selectable */
    .ats-overlay * {
        user-select: text !important;
        -webkit-user-select: text !important;
        -moz-user-select: text !important;
        -ms-user-select: text !important;
    }
    
    /* Make sure the main content is not selectable */
    .container, #main-content, .cv-header, body {
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }
    
    /* Override any existing selection styles */
    * {
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }
    
    .ats-overlay {
        -webkit-user-select: text !important;
        -moz-user-select: text !important;
        -ms-user-select: text !important;
        user-select: text !important;
    }
    </style>
    '''
    
    # Insert ATS CSS before closing head tag
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', f'{ats_css}\n</head>')
    else:
        # If no head tag, add it
        html_content = f'<head>{ats_css}</head>' + html_content
    
    # Create ATS data overlay if data is provided
    if employment_data or education_data or publications_data:
        ats_overlay = create_ats_json_overlay(
            employment_data or [],
            education_data or [],
            publications_data or []
        )
        
        # Insert overlay after body tag
        if '<body>' in html_content:
            html_content = html_content.replace('<body>', f'<body>\n{ats_overlay}')
        else:
            html_content = f'{ats_overlay}\n{html_content}'
    
    return html_content


def convert_html_to_pdf_with_ats(html_path, pdf_path=None, paper_size="A4", 
                                add_page_numbers=True, employment_data=None,
                                education_data=None, publications_data=None):
    """
    Convert an HTML file to ATS-compatible PDF.
    
    Args:
        html_path (str): Path to the HTML file
        pdf_path (str, optional): Path for the PDF output
        paper_size (str, optional): Paper size for the PDF
        add_page_numbers (bool, optional): Whether to add page numbers
        employment_data (list, optional): Employment data for ATS
        education_data (list, optional): Education data for ATS
        publications_data (list, optional): Publications data for ATS
    
    Returns:
        str: Path to the generated PDF file
    """
    
    if not pdf_path:
        if html_path.endswith('.html'):
            pdf_path = os.path.splitext(html_path)[0] + "_ats.pdf"
        else:
            pdf_path = "cv_ats.pdf"
    
    # Read the HTML content
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Make HTML ATS-compatible
    ats_html = modify_html_for_ats_compatibility(
        html_content, employment_data, education_data, publications_data
    )
    
    # Add page numbers CSS if requested
    if add_page_numbers:
        page_number_css = """
        @page {
            @bottom-right {
                content: "Page " counter(page) " of " counter(pages);
                font-family: var(--font-primary);
                font-size: 10pt;
                color: #666;
                padding-right: 10mm;
            }
            size: A4 portrait;
            margin: 20mm 15mm 20mm 15mm;
        }
        """
        ats_html = ats_html.replace('</style>', f'{page_number_css}\n</style>')
    
    # Create a temporary file with the modified HTML content
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as temp_file:
        temp_file.write(ats_html)
        temp_html_path = temp_file.name
    
    try:
        # Convert HTML to PDF
        html = weasyprint.HTML(filename=temp_html_path)
        pdf = html.write_pdf()
        
        # Write the PDF to file
        with open(pdf_path, 'wb') as f:
            f.write(pdf)
        
        print(f"ATS-compatible PDF saved to {pdf_path}")
        return pdf_path
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_html_path):
            os.unlink(temp_html_path)


def convert_html_to_pdf(html_path, pdf_path=None, paper_size="A4", add_page_numbers=True):
    """
    Original PDF conversion function - kept for backward compatibility.
    Convert an HTML file to PDF using WeasyPrint.
    
    Args:
        html_path (str): Path to the HTML file
        pdf_path (str, optional): Path for the PDF output
        paper_size (str, optional): Paper size for the PDF
        add_page_numbers (bool, optional): Whether to add page numbers
    
    Returns:
        str: Path to the generated PDF file
    """
    if not pdf_path:
        # Use input filename with .pdf extension
        if html_path.endswith('.html'):
            pdf_path = os.path.splitext(html_path)[0] + ".pdf"
        else:
            pdf_path = "cv.pdf"
    
    # Read the HTML content
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Add page numbers CSS if requested
    if add_page_numbers:
        page_number_css = """
        @page {
            @bottom-right {
                content: "Page " counter(page) " of " counter(pages);
                font-family: var(--font-primary);
                font-size: 10pt;
                color: #666;
                padding-right: 10mm;
            }
            size: A4 portrait;
            margin: 20mm 15mm 20mm 15mm;
        }
        """
        html_content = html_content.replace('</style>', f'{page_number_css}\n</style>')
    
    # Create a temporary file with the modified HTML content
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as temp_file:
        temp_file.write(html_content)
        temp_html_path = temp_file.name
    
    try:
        # Convert HTML to PDF
        html = weasyprint.HTML(filename=temp_html_path)
        pdf = html.write_pdf()
        
        # Write the PDF to file
        with open(pdf_path, 'wb') as f:
            f.write(pdf)
        
        print(f"PDF saved to {pdf_path}")
        return pdf_path
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_html_path):
            os.unlink(temp_html_path)


def load_json_data_for_ats(cv_directory):
    """
    Load employment, education, and publications data from JSON files.
    
    Args:
        cv_directory (str): Directory containing the CV and JSON files
        
    Returns:
        tuple: (employment_data, education_data, publications_data)
    """
    employment_data = []
    education_data = []
    publications_data = []
    
    # Load employment data
    employment_path = os.path.join(cv_directory, 'employment.json')
    if os.path.exists(employment_path):
        with open(employment_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            employment_data = data.get('employment', [])
    
    # Load education data
    education_path = os.path.join(cv_directory, 'education.json')
    if os.path.exists(education_path):
        with open(education_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            education_data = data.get('education', [])
    
    # Load publications data
    publications_path = os.path.join(cv_directory, 'publications.json')
    if os.path.exists(publications_path):
        with open(publications_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            publications_data = data.get('publications', [])
    
    return employment_data, education_data, publications_data


# Example usage
if __name__ == "__main__":
    # Test the ATS-compatible PDF generation
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test CV</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>John Doe</h1>
            <h2>Software Engineer</h2>
            <p>This is a test CV for ATS compatibility.</p>
        </div>
    </body>
    </html>
    """
    
    # Create test HTML file
    with open('test_cv.html', 'w', encoding='utf-8') as f:
        f.write(sample_html)
    
    # Sample data
    sample_employment = [{"position": "Software Engineer", "company": "Tech Corp"}]
    sample_education = [{"degree": "BS Computer Science", "institution": "University"}]
    sample_publications = [{"title": "Test Paper", "year": 2023}]
    
    # Generate ATS-compatible PDF
    convert_html_to_pdf_with_ats(
        'test_cv.html',
        'test_cv_ats.pdf',
        employment_data=sample_employment,
        education_data=sample_education,
        publications_data=sample_publications
    )
    
    print("Test files created: test_cv.html and test_cv_ats.pdf")
    print("Open the PDF and try selecting text - you should get JSON data instead of visible text!")
