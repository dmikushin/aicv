def escape_latex(text: str) -> str:
    """Sanitizes text for LaTeX by escaping special characters."""
    if not isinstance(text, str):
        text = str(text)

    # Remove or replace characters that are hard to escape or problematic in LaTeX
    text = text.replace('\u2013', '--')  # en-dash
    text = text.replace('\u2014', '---')  # em-dash
    text = text.replace('\u2018', "`")    # left single quote
    text = text.replace('\u2019', "'")    # right single quote
    text = text.replace('\u201c', "``")   # left double quote
    text = text.replace('\u201d', "''")   # right double quote

    # Order of replacements matters to avoid double escaping or incorrect replacements
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        #'\\': r'\textbackslash{}',  # Conflicts with legitimate backslash in LaTeX commands
        '-': r'--',                 # Hyphens to en-dashes for LaTeX text (optional, but good practice)
        '<': r'\textless{}',
        '>': r'\textgreater{}',
        '|': r'\textbar{}',
        '" ': r"'' ",              # Smart quotes (closing)
        ' "': r' ``',              # Smart quotes (opening)
    }

    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text

