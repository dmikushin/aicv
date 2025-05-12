"""
Text processing utilities for the AI-aware CV generator
"""
import re

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

def format_phd_name(name, backend='html'):
    """Format a name with PhD title consistently across backends.
    
    Args:
        name (str): The person's name, may include PhD variants
        backend (str): 'html' or 'markdown'
    
    Returns:
        str: Formatted name with PhD consistently displayed
    """
    has_phd = False
    if name and ('PhD' in name or 'Ph.D' in name or 'Ph.D.' in name):
        has_phd = True
        # Remove PhD from name
        name = re.sub(r',?\s*(PhD|Ph\.D\.?)', '', name)
    
    if has_phd:
        if backend == 'html':
            return f"{name},<br>PhD"
        else:
            return f"{name}, PhD"
    return name

def format_website(website, backend='html'):
    """Format website URL and text consistently across backends.
    
    Args:
        website: String URL or dict with 'url' key
        backend (str): 'html' or 'markdown'
    
    Returns:
        str: Formatted website reference
    """
    if not website:
        return ""
        
    if isinstance(website, dict):
        website_url = website.get('url', '')
    else:
        website_url = website
    
    # Remove protocol for display text
    website_text = re.sub(r'^.*?://', '', website_url)
    
    # Ensure URL has protocol
    if website_url and not website_url.startswith('http'):
        website_url = f"https://{website_url}"
    
    if backend == 'html':
        return f'<a href="{website_url}" target="_blank">{website_text}</a>'
    else:
        return f"[{website_text}]({website_url})"

def format_github(github, backend='html'):
    """Format GitHub username or URL consistently across backends.
    
    Args:
        github (str): GitHub username or URL
        backend (str): 'html' or 'markdown'
    
    Returns:
        str: Formatted GitHub reference
    """
    if not github:
        return ""
    
    # Extract username from URL or handle username directly
    if 'github.com/' in github:
        # Extract username from URL
        username = github.split('github.com/')[-1].strip('/')
    elif github.startswith('@'):
        username = github.lstrip('@')
    else:
        username = github  # Assume it's already a username
    
    # Normalize URL
    github_url = f"https://github.com/{username}"
    
    # Normalize display text to @username format
    github_text = f"@{username}"
    
    if backend == 'html':
        # HTML version with GitHub icon SVG (simplified version)
        github_icon = '<svg width="20" height="20" viewBox="0 0 16 16" style="display:inline-block;vertical-align:middle;fill:currentColor"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>'
        return f'<span class="mono-emoji">{github_icon}</span><a href="{github_url}" target="_blank">{github_text}</a>'
    else:
        return f"[{github_text}]({github_url})"

def format_email(email, backend='html'):
    """Format email address consistently across backends.
    
    Args:
        email (str): Email address
        backend (str): 'html' or 'markdown'
    
    Returns:
        str: Formatted email reference
    """
    if not email:
        return ""
        
    if backend == 'html':
        return f'<a href="mailto:{email}">{email}</a>'
    else:
        return f"[{email}](mailto:{email})"

def format_personal_info(personal_info, field, backend='html'):
    """Format a specific personal info field consistently across backends.
    
    Args:
        personal_info (dict): Personal information dictionary
        field (str): Field name to format
        backend (str): 'html' or 'markdown'
    
    Returns:
        str: Formatted field value
    """
    value = personal_info.get(field, "")
    if not value:
        return ""
        
    if field == 'name':
        return format_phd_name(value, backend)
    elif field == 'website':
        return format_website(value, backend)
    elif field == 'github':
        return format_github(value, backend)
    elif field == 'email':
        return format_email(value, backend)
    else:
        return value
