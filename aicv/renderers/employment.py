"""
Employment section renderer for the AI-aware CV generator
"""
from aicv.utils.escape_latex import escape_latex

def render_employment(employment, backend="markdown", emojis=True):
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
            position_emoji = '💼' if emojis else ''
            position_lower = job['position'].lower()
            if emojis:
                for keyword, emoji in job_emojis.items():
                    if keyword in position_lower:
                        position_emoji = emoji
                        break
            html += f'<div class="employment-entry">'
            html += f'<h2>{(position_emoji + " ") if position_emoji else ""}<span class="job-header">{job["position"]} at {job["company"]}</span></h2>'
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
    elif backend == "markdown":
        md = ""
        for job in employment:
            position_emoji = '💼' if emojis else ''
            position_lower = job['position'].lower()
            if emojis:
                for keyword, emoji in job_emojis.items():
                    if keyword in position_lower:
                        position_emoji = emoji
                        break
            md += f"## {(position_emoji + ' ') if position_emoji else ''}{job['position']} at {job['company']}\n"
            md += f"*{job['dates']}*\n\n"
            if 'location' in job and job['location']:
                md += f"- **Location:** {job.get('location', 'N/A')}\n"
            md += f"- **Responsibilities:**\n\n"
            for responsibility in job['responsibilities']:
                md += f"    - {responsibility}\n"
            md += "\n"
        return md

    elif backend == "moderncv":
        if not employment:
            return ""
        lines = ["\\section{Experience}"]
        for job in employment:
            # Try to get fields with fallback
            start_year = job.get('start_year') or job.get('start') or ''
            end_year = job.get('end_year') or job.get('end') or ''
            year_range = f"{start_year}--{end_year}" if end_year else f"{start_year}"
            title = escape_latex(job.get('position', ''))
            employer = escape_latex(job.get('company', job.get('employer', '')))
            location = escape_latex(job.get('location', ''))
            # Responsibilities as description
            responsibilities = job.get('responsibilities', [])
            if responsibilities:
                description = "\\begin{itemize}\n" + "\n".join([f"\\item {escape_latex(r)}" for r in responsibilities]) + "\n\\end{itemize}"
            else:
                description = ""
            lines.append(f"\\cventry{{{escape_latex(year_range)}}}{{{title}}}{{{employer}}}{{{location}}}{{}}{{\\footnotesize {description}}}")
            # Compose cventry
            lines.append(f"\\cventry{{{escape_latex(year_range)}}}{{{title}}}{{{employer}}}{{{location}}}{{}}{{\\footnotesize {description}}}")
            lines.append("\\vskip 2pt")
        return "\n".join(lines)

    else:
        raise ValueError("Unsupported backend. Use 'html' or 'markdown'.")
