"""
HTML generation utilities for the AI-aware CV generator
"""
import os
import re

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

def create_styled_html(content, personal_info, photo_html):
    """Creates a full HTML document with styling and structure"""

    # Split name into parts for PhD styling if applicable
    name = personal_info['name']
    name_parts = name.split(' ')

    # Check if the person has PhD in their title
    has_phd = False
    if name and ('PhD' in name or 'Ph.D' in name or 'Ph.D.' in name):
        has_phd = True
        # Remove PhD from name
        name = re.sub(r',?\s*(PhD|Ph\.D\.?)', '', name)

    name_with_phd = f"{name},<br>PhD" if has_phd else name

    # Build the document with styling
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - CV</title>
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
                /* For PDF output, we'll keep emojis visible but make them grayscale */
                filter: grayscale(100%);
            }}

            h2 {{
                padding-left: 0;
                /* Ensure page breaks don't occur right after section headings */
                page-break-after: avoid;
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

            /* Avoid orphaned list items */
            li {{
                page-break-inside: avoid;
            }}

            /* Prevent page breaks inside job entries */
            h2 + p + ul {{
                page-break-inside: avoid;
            }}

            /* Ensure contact info doesn't split across pages */
            .contact-info {{
                page-break-inside: avoid;
            }}
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
                    <h1>{name_with_phd}</h1>
                    <div class="position">{personal_info['position']}</div>
                </div>
            </div>
            <div class="header-right">
                <div class="contact-info">
                    <p><span class="mono-emoji">📍</span> {personal_info['address']}</p>
                    <p><span class="mono-emoji">📞</span> {personal_info['phone']}</p>'''

    # Add email with link
    if isinstance(personal_info['email'], dict):
        email_text = personal_info['email']['text']
        email_url = personal_info['email']['url']
        # If it's just an email without a formal protocol, add mailto:
        if '@' in email_url and not email_url.startswith('mailto:') and not email_url.startswith('http'):
            email_url = f"mailto:{email_url}"
        html += f'                    <p><span class="mono-emoji">✉️</span> <a href="{email_url}">{email_text}</a></p>\n'
    else:
        # Fallback for backward compatibility
        html += f'                    <p><span class="mono-emoji">✉️</span> <a href="mailto:{personal_info["email"]}">{personal_info["email"]}</a></p>\n'

    # Add website with link
    if isinstance(personal_info['website'], dict):
        website_text = personal_info['website']['text'].replace('https://', '')
        website_url = personal_info['website']['url']
        # Ensure URL has protocol
        if not website_url.startswith('http'):
            website_url = f"https://{website_url}"
        html += f'                    <p><span class="mono-emoji">🌐</span> <a href="{website_url}" target="_blank">{website_text}</a></p>\n'
    else:
        # Fallback for backward compatibility
        website = personal_info['website'].replace('https://', '')
        html += f'                    <p><span class="mono-emoji">🌐</span> <a href="https://{website}" target="_blank">{website}</a></p>\n'

    # Add GitHub info if available
    if personal_info['github']:
        if isinstance(personal_info['github'], dict):
            github_text = personal_info['github']['text']
            github_url = personal_info['github']['url']
            if not github_url.startswith('http'):
                # Assume it's a username if not a full URL
                if '/' not in github_url and not github_url.startswith('@'):
                    github_url = f"https://github.com/{github_url}"
                elif not github_url.startswith('https://'):
                    github_url = f"https://github.com/{github_url}"
            html += f'                    <p><span class="mono-emoji">💻</span> GitHub: <a href="{github_url}" target="_blank">{github_text}</a></p>\n'
        else:
            # Fallback for backward compatibility
            html += f'                    <p><span class="mono-emoji">💻</span> GitHub: <a href="https://github.com/{personal_info["github"]}" target="_blank">{personal_info["github"]}</a></p>\n'

    # Add date of birth if available
    if personal_info['date_of_birth']:
        html += f'                    <p><span class="mono-emoji">🎂</span> {personal_info["date_of_birth"]}</p>\n'

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
