"""
Education section renderer for the AI-aware CV generator
"""
from aicv.utils.escape_latex import escape_latex
import re

def render_education(education, backend="markdown", emojis=True):
    """Custom rendering of education data with our styling and emojis. Supports markdown and html backends."""

    def get_emoji():
        return "🎓" if emojis else ""

    def format_date_range(edu):
        """Format the date range from start_date and end_date fields"""
        start = edu.get('start_date', '')
        end = edu.get('end_date', '')

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
        for edu in education:
            emoji = get_emoji()
            date_range = format_date_range(edu)

            html += f'<div class="education-entry">'
            html += f'<h2>{emoji + " " if emoji else ""}{edu["degree"]}</h2>'
            html += f'<p class="edu-dates"><em>{date_range}</em></p>'
            html += f'<ul>'
            html += f'<li><strong>Institution:</strong> {edu["institution"]}</li>'
            html += f'<li><strong>Location:</strong> {edu["location"]}</li>'
            if "dissertation" in edu:
                html += f'<li><strong>Dissertation:</strong> {edu["dissertation"]}</li>'
            if "focus_areas" in edu:
                html += f'<li><strong>Focus Areas:</strong> {", ".join(edu["focus_areas"])}</li>'
            if "department" in edu:
                html += f'<li><strong>Department:</strong> {edu["department"]}</li>'
            html += '</ul>'
            html += '</div>\n'
        return html

    elif backend == "markdown":
        md = ""
        for edu in education:
            emoji = get_emoji()
            date_range = format_date_range(edu)

            md += f"## {emoji + ' ' if emoji else ''}{edu['degree']}\n"
            md += f"*{date_range}*\n\n"
            md += f"- **Institution:** {edu['institution']}\n"
            md += f"- **Location:** {edu['location']}\n"
            if "dissertation" in edu:
                md += f"- **Dissertation:** {edu['dissertation']}\n"
            if "focus_areas" in edu:
                md += f"- **Focus Areas:** {', '.join(edu['focus_areas'])}\n"
            if "department" in edu:
                md += f"- **Department:** {edu['department']}\n"
            md += "\n"
        return md

    elif backend == "moderncv":
        lines = []
        for edu in education:
            # Get start and end dates, with fallbacks to old field names
            start_date = edu.get('start_date') or edu.get('start_year') or ''
            end_date = edu.get('end_date') or edu.get('end_year') or ''

            # Extract years only for moderncv
            start_year = extract_year(start_date)
            end_year = extract_year(end_date)

            # Format year range for LaTeX, fallback to old 'dates' field
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

            degree = escape_latex(edu.get("degree", ""))
            institution = escape_latex(edu.get("institution", ""))
            location = escape_latex(edu.get("location", ""))
            description = escape_latex(edu.get("description", ""))
            grade = escape_latex(edu.get("grade", ""))

            # Build extra description
            extra = []
            if "dissertation" in edu and edu["dissertation"]:
                extra.append(f"Dissertation: {escape_latex(edu['dissertation'])}")

            # Render focus_areas as comma-separated
            if "focus_areas" in edu and edu["focus_areas"]:
                extra.append(f"Focus areas: {escape_latex(', '.join(edu['focus_areas']))}")

            # Add department if present
            if "department" in edu and edu["department"]:
                extra.append(f"Department: {escape_latex(edu['department'])}")

            # Compose description
            if extra:
                description = (description + " " if description else "") + "\\\\ ".join(extra)

            # Add cventry
            lines.append(f"\\cventry{{{escape_latex(year_range)}}}{{{degree}}}{{{institution}}}{{{location}}}{{{grade}}}{{{description}}}")
            lines.append("\\vskip 2pt")

        return "\n".join(lines)

    else:
        raise ValueError(f"Unknown backend: {backend}")
