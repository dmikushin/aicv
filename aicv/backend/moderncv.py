"""
LaTeX document generator for the AI-aware CV generator, using moderncv style.
"""
import os
import re
from typing import Dict, Any
from aicv.backend.personal_info import PersonalInfoFormatter
from aicv.utils.escape_latex import escape_latex
from aicv.backend.emojis import EmojisFormatter

class EmojisFormatterModernCV(EmojisFormatter):
    @staticmethod
    def add_section_emojis(content: str) -> str:
        # No emoji for LaTeX by default, but you could add custom logic here
        return content

class PersonalInfoFormatterModernCV(PersonalInfoFormatter):
    def format_website(self) -> str:
        website = self.personal_info.get('website', '')
        website_text, _ = PersonalInfoFormatter.parse_website_info(website)
        if not website_text:
            return ""
        return f"\\homepage{{{website_text}}}"

    def format_linkedin(self) -> str:
        linkedin = self.personal_info.get('linkedin', '')
        username, _ = PersonalInfoFormatter.parse_social_info(linkedin, "https://www.linkedin.com/in/", "", "linkedin.com/in/")
        return f"\\social[linkedin]{{{username}}}"

    def format_github(self) -> str:
        github = self.personal_info.get('github', '')
        username, _ = PersonalInfoFormatter.parse_social_info(github, "https://github.com/", "", "github.com/")
        return f"\\social[github]{{{username}}}"

    def format_email(self) -> str:
        email = self.personal_info.get('email', '')
        if not email:
            return ""
        return f"\\email{{{email}}}"

    def format_phone(self) -> str:
        phone = self.personal_info.get('phone', '')
        if not phone:
            return ""
        return f"\\mobile{{{phone}}}"

    def format_address(self) -> str:
        address = self.personal_info.get('address', '')
        if not address:
            return ""
        return f"\\address{{{escape_latex(address)}}}{{}}{{}}"

def create_moderncv(processed_content, personal_info, bib_content=""):
    """Generates a full LaTeX document string using moderncv.

    Args:
        processed_content (str): The main content of the CV, already formatted as LaTeX sections.
        personal_info (dict): Dictionary containing personal information.
        bib_content (str): BibTeX bibliography content to inline in the document.

    Returns:
        str: A string representing the complete .tex file.
    """
    f = PersonalInfoFormatterModernCV(personal_info)

    firstname = escape_latex(f.format_first_name())
    familyname = escape_latex(f.format_family_name())
    if f.has_phd():
        familyname = f"{familyname}, PhD"

    address = f.format_address()
    mobile = f.format_phone()
    email = f.format_email()
    homepage = f.format_website()
    github = f.format_github()
    linkedin = f.format_linkedin()

    photo_path = personal_info.get('photo', '')
    # Ensure photo path is relative to the tex file or absolute. LaTeX needs forward slashes.
    if photo_path:
        photo_path = photo_path.replace('\\', '/')
        # Check if it's a common image extension, otherwise moderncv might have issues.
        # moderncv typically expects just the name without extension if it's in the search path.
        # For simplicity, we assume the user provides a valid path that pdflatex can find.
        # We might need to copy the photo to the .tex output directory.
        # For now, just use the path. If it's relative, it should be relative to where pdflatex runs.
        photo_cmd = f"\\photo[64pt]{{{photo_path}}}"
    else:
        photo_cmd = "" # No photo command if no photo

    # Bibliography setup - use inline filecontents if bib_content is provided
    bib_filename = "cv_publications.bib"
    bib_setup = ""

    if bib_content:
        # Use filecontents to embed bibliography inline
        bib_setup = f"""
% Inline bibliography using filecontents
\\begin{{filecontents}}[overwrite]{{{bib_filename}}}
{bib_content}
\\end{{filecontents}}
"""

    # Define bibliography environment and commands
    biblatex_setup = f"""
% BibLaTeX for bibliography
\\usepackage[backend=bibtex, style=numeric, sorting=ydnt, maxnames=999, minnames=999]{{biblatex}}
% style=authoryear-comp, bibstyle=authoryear, citestyle=authoryear-comp are other options
% sorting=nyt (name, year, title), ydnt (year (desc), name, title)
\\addbibresource{{{bib_filename}}} % Bib file name

% Define bib environment for moderncv compatibility
\\defbibenvironment{{bibliography}}
{{\\list
  {{\\printtext[labelnumberwidth]{{% label format from numeric.bbx
        \\printfield{{labelprefix}}%
        \\printfield{{labelnumber}}}}}}
  {{\\setlength{{\\labelwidth}}{{\\hintscolumnwidth}}%
    \\advance\\leftmargin\\labelsep}}%
  \\sloppy\\clubpenalty4000\\widowpenalty4000}}
{{\\endlist}}
{{\\item}}
\\renewcommand*{{\\bibnamedash}}{{\\mbox{{\\textemdash\\space}}}}% for repeated authors
% Fix spacing between volume and number fields
\\DeclareFieldFormat[article]{{volume}}{{#1}}
\\DeclareFieldFormat[article]{{number}}{{#1}}
\\renewbibmacro*{{volume+number+eid}}{{%
  \\printfield{{volume}}%
  \\setunit*{{.\\space}}% Add space after period between volume and number
  \\printfield{{number}}%
  \\setunit{{\\addcomma\\space}}%
  \\printfield{{eid}}}}
""" if bib_content else ""

    # Bibliography printing command
    print_bibliography = "\\printbibliography[heading=none]" if bib_content else ""

    # Construct the LaTeX document
    latex_string = f"""
\\documentclass[a4paper]{{moderncv}}
\\moderncvtheme[blue]{{classic}} % or classic, casual, oldstyle
\\usepackage[T2A,T1]{{fontenc}} % T2A for Cyrillic, T1 for Western European
\\usepackage[utf8]{{inputenc}}
\\usepackage[scale=0.86]{{geometry}}
\\usepackage{{comment}} % For multi-line comments if needed

{bib_setup}{biblatex_setup}
\\AtBeginDocument{{\\recomputelengths}} % Recalculate lengths (important)

% Personal Information
\\firstname{{{firstname}}}
\\familyname{{{familyname}}} % moderncv doesn't have a separate title command like this, it's part of familyname

{address}
{mobile}
{email}
{homepage}
{github}
{linkedin}
{photo_cmd}

\\AfterPreamble{{\\hypersetup{{colorlinks,urlcolor=blue}}}} % Make links blue

\\begin{{document}}
\\maketitle

{processed_content} % This will contain \section{{...}} \cventry{{...}} etc.

% Print bibliography if there are publications
{print_bibliography}

\\end{{document}}
"""
    return latex_string
