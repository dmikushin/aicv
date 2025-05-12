"""
Education section renderer for the AI-aware CV generator
"""

def render_education(education, backend="markdown"):
    """Custom rendering of education data with our styling and emojis. Supports markdown and html backends."""
    if backend == "html":
        html = ""
        for edu in education:
            html += f'<div class="education-entry">'
            html += f'<h2>{edu["degree"]}</h2>'
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
    else:
        md = ""
        for edu in education:
            md += f"## {edu['degree']}\n"
            md += f"*{edu['dates']}*\n\n"
            md += f"- **Institution:** {edu['institution']}\n"
            md += f"- **Location:** {edu['location']}\n"
            if "dissertation" in edu:
                md += f"- **Dissertation:** {edu['dissertation']}\n"
            if "focus_areas" in edu:
                md += f"- **Focus Areas:** {', '.join(edu['focus_areas'])}\n"
            md += "\n"
        return md
