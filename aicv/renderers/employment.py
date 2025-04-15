"""
Employment section renderer for the AI-aware CV generator
"""

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

        # Add a special class to mark this as a job header (for avoiding duplicate emojis)
        md += f"## {position_emoji} <span class='job-header'>{job['position']} at {job['company']}</span>\n"

        # Place dates right below the header
        md += f"*{job['dates']}*\n\n"

        # Add location if available
        if 'location' in job and job['location']:
            md += f"- **Location:** {job.get('location', 'N/A')}\n"

        # Add CSS class to control spacing for the responsibilities section
        md += f"- <span class='resp-title'>**Responsibilities:**</span>\n\n"

        # Use proper nesting for responsibilities with 2 spaces indentation
        for responsibility in job['responsibilities']:
            md += f"    - {responsibility}\n"
        md += "\n"
    return md
