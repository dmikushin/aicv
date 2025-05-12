"""
Employment section renderer for the AI-aware CV generator
"""

def render_employment(employment, backend="markdown"):
    """Custom rendering of employment data with our styling and emojis. Supports markdown and html backends."""
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
    if backend == "html":
        html = ""
        for job in employment:
            position_emoji = '💼'  # Default emoji
            position_lower = job['position'].lower()
            for keyword, emoji in job_emojis.items():
                if keyword in position_lower:
                    position_emoji = emoji
                    break
            html += f'<div class="employment-entry">'
            html += f'<h2>{position_emoji} <span class="job-header">{job["position"]} at {job["company"]}</span></h2>'
            html += f'<p class="job-dates"><em>{job["dates"]}</em></p>'
            if 'location' in job and job['location']:
                html += f'<p><strong>Location:</strong> {job["location"]}</p>'
            html += f'<div class="resp-title"><strong>Responsibilities:</strong></div>'
            html += '<ul>'
            for responsibility in job['responsibilities']:
                html += f'<li>{responsibility}</li>'
            html += '</ul>'
            html += '</div>\n'
        return html
    else:
        md = ""
        for job in employment:
            position_emoji = '💼'  # Default emoji
            position_lower = job['position'].lower()
            for keyword, emoji in job_emojis.items():
                if keyword in position_lower:
                    position_emoji = emoji
                    break
            md += f"## {position_emoji} {job['position']} at {job['company']}\n"
            md += f"*{job['dates']}*\n\n"
            if 'location' in job and job['location']:
                md += f"- **Location:** {job.get('location', 'N/A')}\n"
            md += f"- **Responsibilities:**\n\n"
            for responsibility in job['responsibilities']:
                md += f"    - {responsibility}\n"
            md += "\n"
        return md
