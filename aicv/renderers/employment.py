"""
Employment section renderer for the AI-aware CV generator
"""
from aicv.utils.escape_latex import escape_latex
import re

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

    def format_date_range(job):
        """Format the date range from start_date and end_date fields"""
        start = job.get('start_date', '')
        end = job.get('end_date', '')

        if start and end:
            return f"{start} - {end}"
        elif start:
            return f"{start} - Present"
        elif end:
            return f"Until {end}"
        else:
            return ""

    def extract_year(date_string):
        """Extract year from a date string like 'May 2019' or '2019'"""
        if not date_string:
            return ""

        # Handle 'Present' case
        if date_string.lower() == 'present':
            return 'present'

        # Try to extract 4-digit year using regex
        year_match = re.search(r'\b(19|20)\d{2}\b', str(date_string))
        if year_match:
            return year_match.group(0)

        # If no 4-digit year found, return the original string
        return str(date_string)

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

            date_range = format_date_range(job)

            html += f'<div class="employment-entry">'
            html += f'<h2>{(position_emoji + " ") if position_emoji else ""}<span class="job-header">{job["position"]} at {job["company"]}</span></h2>'
            html += f'<p class="job-dates"><em>{date_range}</em></p>'
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

            date_range = format_date_range(job)

            md += f"## {(position_emoji + ' ') if position_emoji else ''}{job['position']} at {job['company']}\n"
            md += f"*{date_range}*\n\n"
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
            # Get start and end dates, with fallbacks to old field names
            start_date = job.get('start_date') or job.get('start_year') or job.get('start') or ''
            end_date = job.get('end_date') or job.get('end_year') or job.get('end') or ''

            # Extract years only for moderncv
            start_year = extract_year(start_date)
            end_year = extract_year(end_date)

            # Format year range for LaTeX
            if start_year and end_year:
                if end_year.lower() == 'present':
                    year_range = f"{start_year}-present"
                else:
                    year_range = f"{start_year}-{end_year}"
            elif start_year:
                year_range = f"{start_year}-present"
            elif end_year:
                year_range = f"-{end_year}"
            else:
                year_range = ""

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
            lines.append("\\vskip 2pt")
        return "\n".join(lines)

    else:
        raise ValueError("Unsupported backend. Use 'html', 'markdown', or 'moderncv'.")
