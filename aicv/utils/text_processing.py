"""
Text processing utilities for the AI-aware CV generator
"""
import re

def remove_personal_info_items(markdown_text):
    """Remove only the basic personal information items from the markdown content that will be displayed in the header."""
    # Define specific fields to remove - only the ones we display in the header
    fields_to_remove = [
        'Name',
        'Position',
        'Address',
        'Phone',
        'Email',
        'Website',
        'Date of Birth'
    ]

    # Create pattern to match only these specific fields
    pattern = r'^\s*\-\s*\*\*(' + '|'.join(fields_to_remove) + r')\*\*:.*?$\n'

    # Remove only the matching lines
    cleaned_text = re.sub(pattern, '', markdown_text, flags=re.MULTILINE)

    # If the first section now starts with blank lines, clean those up
    cleaned_text = re.sub(r'^\s*\n+', '', cleaned_text)

    return cleaned_text


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

    # Extract individual fields from bulleted list at the top of the file
    name_match = re.search(r'\*\*Name\*\*:\s*(.*)', markdown_text)
    if name_match:
        personal_info['name'] = name_match.group(1).strip()

    position_match = re.search(r'\*\*Position\*\*:\s*(.*)', markdown_text)
    if position_match:
        personal_info['position'] = position_match.group(1).strip()

    address_match = re.search(r'\*\*Address\*\*:\s*(.*)', markdown_text)
    if address_match:
        personal_info['address'] = address_match.group(1).strip()

    phone_match = re.search(r'\*\*Phone\*\*:\s*(.*)', markdown_text)
    if phone_match:
        personal_info['phone'] = phone_match.group(1).strip()

    email_match = re.search(r'\*\*Email\*\*:\s*(.*)', markdown_text)
    if email_match:
        personal_info['email'] = extract_link_or_text(email_match.group(1).strip())

    website_match = re.search(r'\*\*Website\*\*:\s*(.*)', markdown_text)
    if website_match:
        personal_info['website'] = extract_link_or_text(website_match.group(1).strip())

    dob_match = re.search(r'\*\*Date of Birth\*\*:\s*(.*)', markdown_text)
    if dob_match:
        personal_info['date_of_birth'] = dob_match.group(1).strip()

    # GitHub might be in a different section, but we'll try to extract it here
    github_match = re.search(r'\*\*GitHub\*\*:\s*(.*)', markdown_text)
    if github_match:
        personal_info['github'] = extract_link_or_text(github_match.group(1).strip())
    else:
        # Some people put this in the website section with GitHub: username, etc.
        if website_match and "github" in website_match.group(1).lower():
            github_username = re.search(r'github\.com/([^/\s]+)', website_match.group(1))
            if github_username:
                personal_info['github'] = github_username.group(1)

    return personal_info


def extract_link_or_text(text):
    """Extract URL and text from markdown link format [text](url) or just return the text"""
    # Check if the text is in markdown link format: [text](url)
    link_pattern = r'\[(.*?)\]\((.*?)\)'
    match = re.search(link_pattern, text)

    if match:
        link_text = match.group(1)
        link_url = match.group(2)
        return {
            'text': link_text,
            'url': link_url
        }
    else:
        return {
            'text': text,
            'url': text  # Just use the text as URL if no explicit markdown link
        }


def convert_markdown_links(html_content):
    """Convert markdown style links [text](url) to HTML links in the content"""
    # Regular expression to find markdown links
    # This pattern looks for [text](url) patterns but avoids matching within HTML tags
    pattern = r'(?<![<"\'])(\[([^\]]+)\]\(([^)]+)\))(?![>"\'])'

    # Replace markdown links with HTML links
    return re.sub(pattern, r'<a href="\3" target="_blank">\2</a>', html_content)


def add_section_emojis(content):
    """Add appropriate emojis to section headers based on their content, but skip job headers"""

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

    # First, we'll process the custom job headers and remove the special class
    # but keep their existing emoji structure
    content = re.sub(
        r'<h2>(.*?)<span class=\'job-header\'>(.*?)</span>(.*?)</h2>',
        r'<h2>\1\2\3</h2>',
        content
    )

    # For all h1 tags and h2 tags that aren't job headers (don't contain the job-header class)
    # We need two separate regex patterns to avoid overwriting job headers

    # Replace h1 tags with ones containing emojis
    content = re.sub(
        r'<h1>(.*?)</h1>',
        lambda m: f'<h1><span class="mono-emoji">{find_emoji(m.group(1))}</span> {m.group(1)}</h1>',
        content
    )

    # Replace h2 tags but only those that don't already have emojis
    # First, capture h2 tags that already have emojis (contain emoji unicode characters)
    emoji_pattern = re.compile(r'<h2>([^<]*?[\U0001F000-\U0001FFFF][^<]*?)</h2>')
    emoji_h2_tags = emoji_pattern.findall(content)

    # Create a safe pattern that doesn't match h2 tags that already have emojis
    # We'll replace only those h2 tags that don't have emojis yet
    for tag in emoji_h2_tags:
        # Replace with a temporary marker
        content = content.replace(f'<h2>{tag}</h2>', f'<h2_EMOJI_ALREADY_PRESENT>{tag}</h2_EMOJI_ALREADY_PRESENT>')

    # Now add emojis to remaining h2 tags
    content = re.sub(
        r'<h2>(.*?)</h2>',
        lambda m: f'<h2><span class="mono-emoji">{find_emoji(m.group(1))}</span> {m.group(1)}</h2>',
        content
    )

    # Restore the temporarily marked tags
    content = re.sub(
        r'<h2_EMOJI_ALREADY_PRESENT>(.*?)</h2_EMOJI_ALREADY_PRESENT>',
        r'<h2>\1</h2>',
        content
    )

    return content
