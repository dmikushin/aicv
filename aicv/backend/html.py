"""
HTML generation utilities for the AI-aware CV generator
"""
import os
import re
import base64
from aicv.backend.personal_info import PersonalInfoFormatter
from aicv.backend.emojis import EmojisFormatter

class EmojisFormatterHtml(EmojisFormatter):
    @staticmethod
    def add_section_emojis(content: str) -> str:
        content = re.sub(
            r'<h1>(.*?)</h1>',
            lambda m: f'<h1><span class="mono-emoji">{EmojisFormatter.find_emoji(m.group(1))}</span> {m.group(1)}</h1>',
            content
        )
        content = re.sub(
            r'<h2>(.*?)</h2>',
            lambda m: f'<h2><span class="mono-emoji">{EmojisFormatter.find_emoji(m.group(1))}</span> {m.group(1)}</h2>',
            content
        )
        return content

class PersonalInfoFormatterHtml(PersonalInfoFormatter):
    def format_website(self) -> str:
        website = self.personal_info.get('website', '')
        website_text, website_url = PersonalInfoFormatter.parse_website_info(website)
        if not website_text:
            return ""
        return f'<a href="{website_url}" target="_blank">{website_text}</a>'

    def format_linkedin(self) -> str:
        linkedin = self.personal_info.get('linkedin', '')
        linkedin_text, linkedin_url = PersonalInfoFormatter.parse_social_info(linkedin, "https://www.linkedin.com/in/", "@", "linkedin.com/in/")
        linkedin_icon = '<svg width="20" height="20" viewBox="0 0 16 16" style="display:inline-block;vertical-align:middle;fill:currentColor"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>'
        return f'<span class="mono-emoji">{linkedin_icon}</span><a href="{linkedin_url}" target="_blank">{linkedin_text}</a>'

    def format_github(self) -> str:
        github = self.personal_info.get('github', '')
        github_text, github_url = PersonalInfoFormatter.parse_social_info(github, "https://github.com/", "@", "github.com/")
        github_icon = '<svg width="20" height="20" viewBox="0 0 16 16" style="display:inline-block;vertical-align:middle;fill:currentColor"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>'
        return f'<span class="mono-emoji">{github_icon}</span><a href="{github_url}" target="_blank">{github_text}</a>'

    def format_email(self) -> str:
        email = self.personal_info.get('email', '')
        if not email:
            return ""
        return f'<a href="mailto:{email}">{email}</a>'

    def format_phone(self) -> str:
        phone = self.personal_info.get('phone', '')
        return phone or ""

    def format_address(self) -> str:
        address = self.personal_info.get('address', '')
        return address or ""

def embed_photo(photo_path):
    """Generates the HTML for the photo section"""
    photo_html = '<div class="photo-placeholder">120 × 150</div>'

    try:
        if os.path.exists(photo_path) and os.path.isfile(photo_path):
            with open(photo_path, "rb") as img_file:
                photo_bytes = img_file.read()
                photo_base64 = base64.b64encode(photo_bytes).decode('utf-8')
                photo_data = f"data:image/jpeg;base64,{photo_base64}"
                photo_html = f'<img src="{photo_data}" alt="photo" style="width: 100%; height: 100%; object-fit: cover;">'
                print(f"Photo found and embedded: {photo_path}")
    except Exception as e:
        print(f"Error processing photo: {e}")

    return photo_html

def create_html_file(html_content, output_path, silent=False):
    """Writes HTML content to a file

    Args:
        html_content (str): The HTML content to write
        output_path (str): The path to write the HTML file to
        silent (bool, optional): If True, don't print message about file creation. Defaults to False.
    """
    with open(output_path, 'w') as f:
        f.write(html_content)
    if not silent:
        print(f"CV saved to {output_path}")

def create_html(content, personal_info, strict_page_breaks=False, emojis=True):
    """Creates a full HTML document with styling and structure
    Args:
        content (str): Main HTML content
        personal_info (dict): Personal info dict
        strict_page_breaks (bool): If True, enforce old page break rules. Default is False (new behavior).
        emojis (bool): Whether to enable emojis in the CV text (except personal info)
    """

    # Embed the photo directly into HTML
    photo_html = embed_photo(personal_info.get('photo', ''))

    f = PersonalInfoFormatterHtml(personal_info)

    # Format name with PhD styling if applicable using the utility function
    simple_name = f.format_name()
    name = simple_name
    if f.has_phd():
        name = f"{name}, PhD"

    # If emojis are disabled, strip all non-personal-info emojis from content
    if not emojis:
        import re
        # Remove emoji spans from section headers and content, but not from personal info
        # Remove <span class="mono-emoji">...</span> in main content (not in contact-info)
        content = re.sub(r'<span class="mono-emoji">[^<]*</span> ?', '', content)
        # Remove leading unicode emoji in h2/h3/ul/li, etc.
        content = re.sub(r'(<h[12][^>]*>|<li[^>]*>|^)[\U0001F300-\U0001FAFF\U00002700-\U000027BF\U00002600-\U000026FF\U0001F000-\U0001FFFF] ?','\\1', content)

    # Build the document with styling
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{simple_name} - CV</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary-color: #3465a4;
            --secondary-color: #4e9a06;
            --text-color: #333;
            --secondary-text: #555;
            --light-gray: #f5f5f5;
            --border-color: #ddd;
            --section-spacing: 2rem;
            --timeline-color: var(--primary-color);
            --font-primary: 'EB Garamond', Georgia, 'Times New Roman', Times, serif;
            --line-height: 1.4;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            text-rendering: optimizeLegibility;
        }}

        body {{
            font-family: var(--font-primary);
            font-weight: 400;
            line-height: var(--line-height);
            color: var(--text-color);
            background-color: #fff;
            padding: 0;
            margin: 0;
            font-size: 16px;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 3rem 2rem 2rem;
            background-color: #fff;
        }}

        .cv-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1.5rem;
            border-bottom: none;
            padding-bottom: 1rem;
        }}

        .header-left {{
            display: flex;
            align-items: flex-start;
            flex: 1;
        }}

        .photo-container {{
            width: 120px;
            height: 150px;
            border: 1px solid var(--border-color);
            background-color: var(--light-gray);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 1.5rem;
        }}

        .photo-container img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .photo-placeholder {{
            color: #999;
            font-size: 0.8rem;
            text-align: center;
        }}

        .name-position {{
            flex: 1;
        }}

        .header-right {{
            display: flex;
            justify-content: flex-end;
            align-items: flex-start;
        }}

        .contact-info {{
            font-size: 0.9rem;
            line-height: 1.3;
            text-align: right;
        }}

        .contact-info p {{
            margin-bottom: 0.2rem;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            justify-content: flex-end;
        }}

        .mono-emoji {{
            opacity: 0.7;
            font-size: 1rem;
            margin-right: 0.3rem;
            filter: grayscale(100%);
            display: inline-block;
            vertical-align: text-bottom;
        }}

        .contact-info .mono-emoji {{
            display: inline-block;
            width: 1.2rem;
            text-align: center;
            margin-right: 0.5rem;
        }}

        h1 .mono-emoji, h2 .mono-emoji {{
            opacity: 0.7;
        }}

        h1 {{
            font-size: 2.5rem;
            margin-bottom: 0;
            color: var(--text-color);
            font-weight: 400;
            line-height: 1.1;
        }}

        h2 {{
            font-size: 1.4rem;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
            color: var(--primary-color);
            padding-bottom: 0.3rem;
            border-bottom: 2px solid var(--primary-color);
            font-weight: 400;
            text-transform: uppercase;
        }}

        h3 {{
            font-size: 1.2rem;
            margin-top: 1rem;
            margin-bottom: 0.5rem;
            font-weight: 400;
        }}

        .position {{
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
            font-weight: 400;
            color: var(--text-color);
        }}

        .status-note {{
            display: inline-block;
            background-color: var(--light-gray);
            color: var(--text-color);
            padding: 0.3rem 0.5rem;
            font-size: 0.9rem;
            margin-top: 0.5rem;
            font-weight: 400;
        }}

        #main-content {{
            margin-bottom: 1.5rem;
        }}

        .core-competency {{
            margin-bottom: 1rem;
        }}

        .core-competency strong {{
            font-size: 1rem;
            display: block;
            margin-bottom: 0.2rem;
            font-weight: 500;
        }}

        .core-competency p {{
            margin-top: 0;
            line-height: 1.4;
            margin-bottom: 0.5rem;
        }}

        ul {{
            margin-bottom: 1rem;
            padding-left: 1.5rem;
        }}

        li {{
            margin-bottom: 0.4rem;
            position: relative;
        }}

        .resp-title {{
            display: block;
            margin-bottom: 0.4rem; /* Match the spacing between other list items */
        }}

        /* Style for the dates immediately below job header */
        h2 + p em {{
            display: block;
            color: var(--primary-color); /* Same blue color as the headers */
            font-size: 1.2rem; /* Larger font size */
            margin-top: -0.5rem;
            margin-bottom: 1rem;
        }}

        /* Make sure the job title stands out more */
        .job-header {{
            font-weight: 500;
        }}

        /* Add more spacing before the responsibilities */
        .resp-title {{
            margin-top: 0.5rem;
        }}

        /* Ensure consistent spacing for all list items */
        li {{
            margin-bottom: 0.4rem;
        }}

        .timeline {{
            position: relative;
            padding-left: 0;
        }}

        .timeline::before {{
            display: none;
        }}

        .timeline-item {{
            position: relative;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
        }}

        .timeline-item::before {{
            display: none;
        }}

        .timeline-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.3rem;
            flex-wrap: wrap;
        }}

        .timeline-title {{
            font-weight: 500;
            font-size: 1.1rem;
            margin-bottom: 0.2rem;
            margin-right: 1rem;
        }}

        .timeline-date {{
            color: #666;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
        }}

        .timeline-location {{
            margin-bottom: 0.4rem;
            font-style: italic;
            color: #666;
            font-size: 0.95rem;
        }}

        .job-date-line {{
            position: relative;
            margin-top: -10px;
            margin-bottom: 15px;
            border-top: 2px solid var(--primary-color);
        }}

        .job-date {{
            position: relative;
            top: -0.7em;
            float: right;
            background-color: #fff;
            padding: 0 5px;
            color: #666;
            font-size: 0.9rem;
            font-style: italic;
        }}

        .publications-list li {{
            margin-bottom: 0.75rem;
            font-size: 0.95rem;
        }}

        .publications-list li {{
            margin-bottom: 0.75rem;
            font-size: 0.95rem;
        }}

        .skills {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
        }}

        .skill-category {{
            margin-bottom: 0.75rem;
        }}

        .skill-title {{
            font-weight: 500;
            margin-bottom: 0.2rem;
        }}

        .skill-list {{
            color: #555;
            line-height: 1.3;
            font-size: 0.95rem;
        }}

        p {{
            margin-bottom: 0.75rem;
        }}

        .section-heading {{
            position: relative;
            overflow: hidden;
            margin-bottom: 1rem;
        }}

        .section-heading::after {{
            content: '';
            display: block;
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 2px;
            background-color: var(--primary-color);
        }}

        .experience-dates {{
            color: #666;
            font-weight: 400;
            min-width: 6rem;
            display: inline-block;
            text-align: right;
            padding-right: 1rem;
        }}

        /* Fix styling issues in generated content */
        #main-content h1 {{
            font-size: 1.8rem;
            margin-top: 2rem;
            color: var(--primary-color);
            text-transform: uppercase;
            border-bottom: 2px solid var(--primary-color);
            padding-bottom: 0.3rem;
        }}

        #main-content h2 {{
            font-size: 1.2rem;
            margin-top: 1.5rem;
            text-transform: none;
        }}

        /* Add styling for links */
        a {{
            color: var(--primary-color);
            text-decoration: none;
            transition: color 0.2s ease;
        }}

        a:hover {{
            color: var(--secondary-color);
            text-decoration: underline;
        }}

        /* PDF-specific styles */
        @page {{
            size: A4 portrait;
            margin: 20mm 15mm 20mm 15mm;
        }}

        @media print {{
            .mono-emoji {{
                filter: grayscale(100%);
            }}

            h2 {{
                padding-left: 0;
                {'page-break-after: avoid;' if strict_page_breaks else ''}
            }}

            body {{
                font-size: 10pt;
                background: none;
                color: black;
            }}

            .container {{
                max-width: 100%;
                margin: 0;
                padding: 0;
                box-shadow: none;
            }}

            a {{
                text-decoration: none;
                color: black;
            }}

            .photo-container {{
                border: 1px solid #000;
            }}

            h2 {{
                color: black;
                border-bottom-color: black;
            }}

            {'li { page-break-inside: avoid; }' if strict_page_breaks else ''}
            {'h2 + p + ul { page-break-inside: avoid; }' if strict_page_breaks else ''}
            {'.contact-info { page-break-inside: avoid; }' if strict_page_breaks else ''}
        }}

        @media (max-width: 768px) {{
            .cv-header {{
                flex-direction: column;
            }}

            .header-left {{
                align-self: center;
                margin-right: 0;
                margin-bottom: 1rem;
                flex-direction: column;
                align-items: center;
            }}

            .photo-container {{
                margin-right: 0;
                margin-bottom: 1rem;
            }}

            .name-position {{
                text-align: center;
            }}

            .header-right {{
                flex-direction: column;
                align-items: center;
            }}

            .contact-info {{
                text-align: center;
                margin-right: 0;
                margin-bottom: 1rem;
            }}

            .contact-info p {{
                justify-content: center;
            }}

            h1 {{
                font-size: 2rem;
                text-align: center;
            }}

            .skills {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="cv-header">
            <div class="header-left">
                <div class="photo-container">
                    {photo_html}
                </div>
                <div class="name-position">
                    <h1>{name}</h1>
                    <div class="position">{personal_info.get('position', '')}</div>
                </div>
            </div>
            <div class="header-right">
                <div class="contact-info">
                    <p><span class="mono-emoji">📍</span> {f.format_address()}</p>
                    <p><span class="mono-emoji">📞</span> {f.format_phone()}</p>'''

    html += f'                    <p><span class="mono-emoji">✉️</span> {f.format_email()}</p>\n'
    html += f'                    <p><span class="mono-emoji">🌐</span> {f.format_website()}</p>\n'
    html += f'                    <p><span class="mono-emoji"></span> {f.format_github()}</p>\n'
    html += f'                    <p><span class="mono-emoji">🎂</span> {f.format_date_of_birth()}</p>\n'
    html += '''                </div>
            </div>
        </header>

        <div id="main-content">
'''

    # Add the main content
    html += content

    html += '''
        </div>
    </div>
</body>
</html>
'''

    return html
