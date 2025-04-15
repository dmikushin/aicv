"""
Education section renderer for the AI-aware CV generator
"""

def render_education(education):
    """Custom rendering of education data with our styling and emojis"""
    md = "## Education\n"
    for edu in education:
        md += f"## {edu['degree']}\n"

        # Place dates right below the header, using the same format as employment dates
        md += f"<p><em>{edu['dates']}</em></p>\n\n"

        md += f"- **Institution:** {edu['institution']}\n"
        md += f"- **Location:** {edu['location']}\n"

        if "dissertation" in edu:
            md += f"- **Dissertation:** {edu['dissertation']}\n"
        if "focus_areas" in edu:
            md += f"- **Focus Areas:** {', '.join(edu['focus_areas'])}\n"
        md += "\n"
    return md
