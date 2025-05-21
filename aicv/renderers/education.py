"""
Education section renderer for the AI-aware CV generator
"""
from aicv.utils.escape_latex import escape_latex

def render_education(education, backend="markdown", emojis=True):
    """Custom rendering of education data with our styling and emojis. Supports markdown and html backends."""
    def get_emoji():
        return "🎓" if emojis else ""
    if backend == "html":
        html = ""
        for edu in education:
            emoji = get_emoji()
            html += f'<div class="education-entry">'
            html += f'<h2>{emoji + " " if emoji else ""}{edu["degree"]}</h2>'
            html += f'<p class="edu-dates"><em>{edu["dates"]}</em></p>'
            html += f'<ul>'
            html += f'<li><strong>Institution:</strong> {edu["institution"]}</li>'
            html += f'<li><strong>Location:</strong> {edu["location"]}</li>'
            if "dissertation" in edu:
                html += f'<li><strong>Dissertation:</strong> {edu["dissertation"]}</li>'
            if "focus_areas" in edu:
                html += f'<li><strong>Focus Areas:</strong> {", ".join(edu["focus_areas"])}</li>'
            html += '</ul>'
            html += '</div>\n'
        return html
    elif backend == "markdown":
        md = ""
        for edu in education:
            emoji = get_emoji()
            md += f"## {emoji + ' ' if emoji else ''}{edu['degree']}\n"
            md += f"*{edu['dates']}*\n\n"
            md += f"- **Institution:** {edu['institution']}\n"
            md += f"- **Location:** {edu['location']}\n"
            if "dissertation" in edu:
                md += f"- **Dissertation:** {edu['dissertation']}\n"
            if "focus_areas" in edu:
                md += f"- **Focus Areas:** {', '.join(edu['focus_areas'])}\n"
            md += "\n"
        return md

    elif backend == "moderncv":
        lines = ["\\section{Education}"]
        for edu in education:
            # Support both dict and object (for compatibility)
            get = lambda k: edu.get(k, "")
            year_range = escape_latex(get("dates") if "dates" in edu else f"{get('start_year')}--{get('end_year')}" if get('end_year') else get('start_year'))
            degree = escape_latex(get("degree"))
            institution = escape_latex(get("institution"))
            location = escape_latex(get("location") if get("location") else "")
            description = escape_latex(get("description") if get("description") else "")
            grade = escape_latex(get("grade") if get("grade") else "")

            # Build extra description
            extra = []
            if "dissertation" in edu and edu["dissertation"]:
                extra.append(f"Dissertation: {escape_latex(edu['dissertation'])}")

            # Render focus_areas as comma-separated
            if "focus_areas" in edu and edu["focus_areas"]:
                extra.append(f"Focus areas: {escape_latex(', '.join(edu['focus_areas']))}")

            # Compose description
            if extra:
                description = (description + " " if description else "") + "\\\\ ".join(extra)

            # Add cventry
            lines.append(f"\\cventry{{{year_range}}}{{{degree}}}{{{institution}}}{{{location}}}{{{grade}}}{{{description}}}")
            lines.append("\\vskip 2pt")

        return "\n".join(lines)

    else:
        raise ValueError(f"Unknown backend: {backend}")    
