import argparse
import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re
import io
import sys
import json
import os

class PyMdExtension(Extension):
    """A custom Markdown extension to handle `pymd` blocks.
    """
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.register(PyMdPreprocessor(md), 'pymd', 175)


class PyMdPreprocessor(Preprocessor):
    """A preprocessor that identifies `pymd` blocks, executes the Python code within them, and replaces the block with the result."""
    def run(self, lines):
        new_lines = []
        pymd_block = False
        pymd_code = []

        for line in lines:
            if line.strip().startswith('```pymd'):
                pymd_block = True
                pymd_code = []
            elif line.strip() == '```' and pymd_block:
                pymd_block = False
                # Redirect stdout to capture the output of the executed code
                old_stdout = sys.stdout
                sys.stdout = io.StringIO()
                try:
                    # Pass the current global namespace to exec
                    exec('\n'.join(pymd_code), globals())
                    # Get the output and append it to new_lines
                    output = sys.stdout.getvalue()
                    new_lines.extend(output.splitlines())
                finally:
                    sys.stdout = old_stdout
            elif pymd_block:
                pymd_code.append(line)
            else:
                new_lines.append(line)

        return new_lines


def process_markdown(file_path):
    """Reads a Markdown file, processes it with the custom extension, and returns the processed content.
    """
    with open(file_path, 'r') as f:
        text = f.read()

    md = markdown.Markdown(extensions=[PyMdExtension()])
    html_content = md.convert(text)

    # Extract personal information from the markdown text
    personal_info = extract_personal_info(text)

    # Create full HTML document with styling
    html_document = create_styled_html(html_content, personal_info)

    return html_document


def extract_personal_info(markdown_text):
    """Extract personal information from markdown text for the header section"""
    personal_info = {
        'name': '',
        'position': '',
        'address': '',
        'phone': '',
        'email': '',
        'website': '',
        'date_of_birth': '',
        'github': ''
    }

    # Find the Personal Information section
    personal_section_match = re.search(r'## PERSONAL INFORMATION(.*?)(?=^##|\Z)',
                                     markdown_text, re.MULTILINE | re.DOTALL)

    if personal_section_match:
        personal_section = personal_section_match.group(1)

        # Extract individual fields
        name_match = re.search(r'\*\*Name\*\*:\s*(.*)', personal_section)
        if name_match:
            personal_info['name'] = name_match.group(1).strip()

        position_match = re.search(r'\*\*Position\*\*:\s*(.*)', personal_section)
        if position_match:
            personal_info['position'] = position_match.group(1).strip()

        address_match = re.search(r'\*\*Address\*\*:\s*(.*)', personal_section)
        if address_match:
            personal_info['address'] = address_match.group(1).strip()

        phone_match = re.search(r'\*\*Phone\*\*:\s*(.*)', personal_section)
        if phone_match:
            personal_info['phone'] = phone_match.group(1).strip()

        email_match = re.search(r'\*\*Email\*\*:\s*(.*)', personal_section)
        if email_match:
            personal_info['email'] = email_match.group(1).strip()

        website_match = re.search(r'\*\*Website\*\*:\s*(.*)', personal_section)
        if website_match:
            personal_info['website'] = website_match.group(1).strip()

        dob_match = re.search(r'\*\*Date of Birth\*\*:\s*(.*)', personal_section)
        if dob_match:
            personal_info['date_of_birth'] = dob_match.group(1).strip()

        # GitHub might be in a different section, but we'll try to extract it here
        github_match = re.search(r'\*\*GitHub\*\*:\s*(.*)', personal_section)
        if github_match:
            personal_info['github'] = github_match.group(1).strip()
        else:
            # Some people put this in the website section with GitHub: username, etc.
            if website_match and "github" in website_match.group(1).lower():
                github_username = re.search(r'github\.com/([^/\s]+)', website_match.group(1))
                if github_username:
                    personal_info['github'] = github_username.group(1)

    return personal_info


def create_styled_html(content, personal_info):
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
            flex: 1;
            margin-right: 2rem;
        }}

        .header-right {{
            display: flex;
            justify-content: flex-end;
            align-items: flex-start;
        }}

        .contact-info {{
            margin-right: 1.5rem;
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

        .photo-container {{
            width: 120px;
            height: 150px;
            border: 1px solid var(--border-color);
            background-color: var(--light-gray);
            display: flex;
            align-items: center;
            justify-content: center;
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

        @media print {{
            .mono-emoji {{
                display: none;
            }}

            h2 {{
                padding-left: 0;
            }}

            body {{
                font-size: 10pt;
                background: none;
                color: black;
            }}

            .container {{
                max-width: 100%;
                margin: 0;
                padding: 2cm 0.5cm 0.5cm;
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
        }}

        @media (max-width: 768px) {{
            .cv-header {{
                flex-direction: column;
            }}

            .header-left {{
                align-self: center;
                margin-right: 0;
                margin-bottom: 1rem;
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

            .photo-container {{
                margin: 0;
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
                <h1>{name_with_phd}</h1>
            </div>
            <div class="header-right">
                <div class="contact-info">
                    <p><span class="mono-emoji">📍</span> {personal_info['address']}</p>
                    <p><span class="mono-emoji">📞</span> {personal_info['phone']}</p>
                    <p><span class="mono-emoji">✉️</span> {personal_info['email']}</p>
                    <p><span class="mono-emoji">🌐</span> {personal_info['website'].replace('https://', '')}</p>
'''

    # Add GitHub info if available
    if personal_info['github']:
        html += f'                    <p><span class="mono-emoji">💻</span> GitHub: {personal_info["github"]}</p>\n'

    # Add date of birth if available
    if personal_info['date_of_birth']:
        html += f'                    <p><span class="mono-emoji">🎂</span> {personal_info["date_of_birth"]}</p>\n'

    html += '''                </div>
                <div class="photo-container">
                    <div class="photo-placeholder">120 × 150</div>
                </div>
            </div>
        </header>

        <div id="main-content">
'''

    # Process the content to add section emojis
    content = add_section_emojis(content)
    html += content

    html += '''
        </div>
    </div>

    <script>
        // Function to handle photo upload
        function setupPhotoUpload() {
            const photoContainer = document.querySelector('.photo-container');

            photoContainer.addEventListener('click', function() {
                const input = document.createElement('input');
                input.type = 'file';
                input.accept = 'image/*';

                input.onchange = function(e) {
                    const file = e.target.files[0];
                    if (file) {
                        const reader = new FileReader();
                        reader.onload = function(event) {
                            const img = photoContainer.querySelector('img') || document.createElement('img');
                            img.src = event.target.result;
                            img.style.width = '100%';
                            img.style.height = '100%';
                            img.style.objectFit = 'cover';

                            if (!photoContainer.querySelector('img')) {
                                photoContainer.innerHTML = '';
                                photoContainer.appendChild(img);
                            }
                        };
                        reader.readAsDataURL(file);
                    }
                };

                input.click();
            });

            // Add hover effect
            photoContainer.addEventListener('mouseenter', function() {
                this.style.cursor = 'pointer';
                this.style.opacity = '0.9';
            });

            photoContainer.addEventListener('mouseleave', function() {
                this.style.opacity = '1';
            });
        }

        // Initialize photo upload functionality
        document.addEventListener('DOMContentLoaded', function() {
            setupPhotoUpload();
        });
    </script>
</body>
</html>
'''

    return html


def add_section_emojis(content):
    """Add appropriate emojis to section headers based on their content"""

    # Define a mapping of section keywords to emojis
    section_emojis = {
        'academic': '🎓',
        'education': '🎓',
        'professional': '💼',
        'experience': '💼',
        'employment': '💼',
        'work': '💼',
        'award': '🏆',
        'skill': '🔧',
        'competenc': '🔧',  # Matches competencies, competence
        'technolog': '💻',  # Matches technology, technologies
        'language': '🗣️',
        'publication': '📚',
        'research': '🔬',
        'project': '📋',
        'interest': '⚡',
        'hobby': '⚡',
        'phd': '📝',
        'thesis': '📄',
        'certification': '🏅',
        'volunteer': '🤝',
        'achievement': '🏆'
    }

    # Function to find the appropriate emoji for a heading
    def find_emoji(heading_text):
        heading_lower = heading_text.lower()
        for keyword, emoji in section_emojis.items():
            if keyword in heading_lower:
                return emoji
        return '📄'  # Default emoji if no match

    # Replace h1 and h2 tags with ones containing emojis
    content = re.sub(
        r'<h1>(.*?)</h1>',
        lambda m: f'<h1><span class="mono-emoji">{find_emoji(m.group(1))}</span> {m.group(1)}</h1>',
        content
    )

    content = re.sub(
        r'<h2>(.*?)</h2>',
        lambda m: f'<h2><span class="mono-emoji">{find_emoji(m.group(1))}</span> {m.group(1)}</h2>',
        content
    )

    return content


def render(json_filename):
    """Reads a JSON file and renders the content based on its type."""
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


def render_education(education):
    """Custom rendering of education data with our styling and emojis"""
    md = "## Education\n"
    for edu in education:
        md += f"## {edu['degree']}\n"
        md += f"- **Institution:** {edu['institution']}\n"
        md += f"- **Location:** {edu['location']}\n"
        md += f"- **Dates:** {edu['dates']}\n"
        if "dissertation" in edu:
            md += f"- **Dissertation:** {edu['dissertation']}\n"
        if "focus_areas" in edu:
            md += f"- **Focus Areas:** {', '.join(edu['focus_areas'])}\n"
        md += "\n"
    return md


def render_employment(employment):
    """Custom rendering of employment data with our styling and emojis"""
    md = ""

    # Define emoji mapping for job positions
    job_emojis = {
        'developer': '💻',
        'engineer': '🛠️',
        'researcher': '🔬',
        'scientist': '🧪',
        'manager': '👔',
        'lead': '👑',
        'founder': '🚀',
        'ceo': '🚀',
        'cto': '🚀',
        'director': '👑',
        'consultant': '💼',
        'specialist': '🔍',
        'architect': '🏛️',
        'professor': '🎓',
        'teacher': '🎓',
        'instructor': '🎓',
        'assistant': '📋',
        'intern': '🌱',
        'analyst': '📊',
        'designer': '🎨'
    }

    for job in employment:
        # Find appropriate emoji for job position
        position_emoji = '💼'  # Default emoji
        position_lower = job['position'].lower()
        for keyword, emoji in job_emojis.items():
            if keyword in position_lower:
                position_emoji = emoji
                break

        md += f"## {position_emoji} {job['position']} at {job['company']}\n"
        md += f"- **Location:** {job.get('location', 'N/A')}\n"
        md += f"- **Dates:** {job['dates']}\n"
        md += "- **Responsibilities:**\n"
        for responsibility in job['responsibilities']:
            md += f"  - {responsibility}\n"
        md += "\n"
    return md


def render_publications(publications):
    """
    Custom rendering of publications data with our styling and emojis.
    Publications are sorted by citation count in descending order.
    """
    # Sort publications by the number of citations in descending order
    sorted_publications = sorted(publications, key=lambda pub: pub.get('citations', 0), reverse=True)

    md = "## Publications (peer-reviewed)\n\n"

    # Format each publication according to its type
    for pub in sorted_publications:
        pub_type = pub.get('type', 'article')

        # Select emoji based on citation count
        citation_count = pub.get('citations', 0)
        if citation_count > 30:
            citation_emoji = "🌟"
        elif citation_count > 15:
            citation_emoji = "⭐"
        elif citation_count > 5:
            citation_emoji = "📊"
        else:
            citation_emoji = "📄"

        # Format authors in a consistent way: "Last1, F., Last2, F., & Last3, F."
        authors = []
        for author in pub['author']:
            # Handle cases where author is already in "Last, First" format
            if "," in author:
                parts = author.split(",", 1)
                last_name = parts[0].strip()
                first_name = parts[1].strip() if len(parts) > 1 else ""
                if first_name:
                    # Use first initial only
                    first_initial = first_name[0]
                    authors.append(f"{last_name}, {first_initial}.")
                else:
                    authors.append(last_name)
            else:
                # Handle cases where author is in "First Last" format
                parts = author.split()
                if len(parts) >= 2:
                    last_name = parts[-1]
                    first_initial = parts[0][0]
                    authors.append(f"{last_name}, {first_initial}.")
                else:
                    authors.append(author)

        # Join authors with commas and "and" for the last author
        if len(authors) > 1:
            authors_text = ", ".join(authors[:-1]) + ", & " + authors[-1]
        else:
            authors_text = authors[0] if authors else ""

        citation = ""
        if pub_type == "article":
            # Format for journal articles: Author(s). (Year). Title. Journal, Volume(Number), Pages.
            citation = f"{citation_emoji} {authors_text} ({pub['year']}). {pub['title']}. "

            if 'journal' in pub:
                citation += f"*{pub['journal']}*"

                if 'volume' in pub:
                    citation += f", {pub['volume']}"

                if 'number' in pub:
                    citation += f"({pub['number']})"

                if 'pages' in pub and pub['pages']:
                    citation += f", {pub['pages']}"

                citation += "."

                if 'publisher' in pub and pub['publisher']:
                    citation += f" {pub['publisher']}."
            else:
                # For articles without a journal specified
                citation += "."

        elif pub_type == "inproceedings":
            # Format for conference proceedings: Author(s). (Year). Title. In Proceedings, Pages.
            citation = f"{citation_emoji} {authors_text} ({pub['year']}). {pub['title']}. "

            if 'booktitle' in pub:
                citation += f"In *{pub['booktitle']}*"

                if 'pages' in pub and pub['pages']:
                    citation += f", pp. {pub['pages']}"

                citation += "."

                if 'organization' in pub and pub['organization']:
                    citation += f" {pub['organization']}."
            else:
                citation += "."

        elif pub_type == "inbook":
            # Format for book chapters: Author(s). (Year). Title. In Book Title, Pages.
            citation = f"{citation_emoji} {authors_text} ({pub['year']}). {pub['title']}. "

            if 'booktitle' in pub:
                citation += f"In *{pub['booktitle']}*"

                if 'pages' in pub and pub['pages']:
                    citation += f", pp. {pub['pages']}"

                citation += "."

                if 'note' in pub and pub['note']:
                    citation += f" {pub['note']}."
            else:
                citation += "."

        # Add citation count if available
        if 'citations' in pub and pub['citations'] > 0:
            citation += f" (Cited {pub['citations']} times)"

        md += f"- {citation}\n"

    return md


def create_html_file(html_content, output_path):
    """Writes HTML content to a file"""
    with open(output_path, 'w') as f:
        f.write(html_content)
    print(f"CV saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a Markdown file with pymd blocks.')
    parser.add_argument('file_path', type=str, help='Path to the Markdown file')
    parser.add_argument('--output', '-o', type=str, help='Output HTML file path (default: input_file.html)')
    args = parser.parse_args()

    # Process the markdown file
    html_content = process_markdown(args.file_path)

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        # Use input filename with .html extension
        base_name = os.path.splitext(args.file_path)[0]
        output_path = f"{base_name}.html"

    # Create the HTML file
    create_html_file(html_content, output_path)
