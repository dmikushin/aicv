import argparse
import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re
import io
import sys
import json

class PyMdExtension(Extension):
    """A custom Markdown extension to handle `pymd` blocks.
    """
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.register(PyMdPreprocessor(md), 'pymd', 175)


class PyMdPreprocessor(Preprocessor):
    """A preprocessor that identifies `pymd` blocks, executes the Python code within them, and replaces the block with the result."""
    def run(self, lines):
        new_lines = []
        pymd_block = False
        pymd_code = []

        for line in lines:
            if line.strip().startswith('```pymd'):
                pymd_block = True
                pymd_code = []
            elif line.strip() == '```' and pymd_block:
                pymd_block = False
                # Redirect stdout to capture the output of the executed code
                old_stdout = sys.stdout
                sys.stdout = io.StringIO()
                try:
                    # Pass the current global namespace to exec
                    exec('\n'.join(pymd_code), globals())
                    # Get the output and append it to new_lines
                    output = sys.stdout.getvalue()
                    new_lines.extend(output.splitlines())
                finally:
                    sys.stdout = old_stdout
            elif pymd_block:
                pymd_code.append(line)
            else:
                new_lines.append(line)

        return new_lines


def process_markdown(file_path):
    """Reads a Markdown file, processes it with the custom extension, and returns the processed content.
    """
    with open(file_path, 'r') as f:
        text = f.read()

    md = markdown.Markdown(extensions=[PyMdExtension()])
    html = md.convert(text)
    return html


def render(json_filename):
    """Reads a JSON file and renders the content based on its type."""
    with open(json_filename, 'r') as f:
        data = json.load(f)

    if "education" in data:
        print(render_education(data["education"]))
    elif "employment" in data:
        print(render_employment(data["employment"]))
    elif "publications" in data:
        print(render_publications(data["publications"]))
    else:
        print("Invalid data format.")


def render_education(education):
    md = "# Education\n"
    for edu in education:
        md += f"## {edu['degree']}\n"
        md += f"- **Institution:** {edu['institution']}\n"
        md += f"- **Location:** {edu['location']}\n"
        md += f"- **Dates:** {edu['dates']}\n"
        if "dissertation" in edu:
            md += f"- **Dissertation:** {edu['dissertation']}\n"
        if "focus_areas" in edu:
            md += f"- **Focus Areas:** {', '.join(edu['focus_areas'])}\n"
        md += "\n"
    return md


def render_employment(employment):
    md = "# Employment\n"
    for job in employment:
        md += f"## {job['position']} at {job['company']}\n"
        md += f"- **Location:** {job.get('location', 'N/A')}\n"
        md += f"- **Dates:** {job['dates']}\n"
        md += "- **Responsibilities:**\n"
        for responsibility in job['responsibilities']:
            md += f"  - {responsibility}\n"
        md += "\n"
    return md


def render_publications(publications):
    """
    Renders publications in commonly accepted academic citation formats based on publication type.
    Publications are sorted by citation count in descending order.
    """
    # Sort publications by the number of citations in descending order
    sorted_publications = sorted(publications, key=lambda pub: pub.get('citations', 0), reverse=True)

    md = "# Publications\n\n"
    md += "## Peer-Reviewed Publications\n\n"

    # Format each publication according to its type
    for pub in sorted_publications:
        pub_type = pub.get('type', 'article')

        # Format authors in a consistent way: "Last1, F., Last2, F., & Last3, F."
        authors = []
        for author in pub['author']:
            # Handle cases where author is already in "Last, First" format
            if "," in author:
                parts = author.split(",", 1)
                last_name = parts[0].strip()
                first_name = parts[1].strip() if len(parts) > 1 else ""
                if first_name:
                    # Use first initial only
                    first_initial = first_name[0]
                    authors.append(f"{last_name}, {first_initial}.")
                else:
                    authors.append(last_name)
            else:
                # Handle cases where author is in "First Last" format
                parts = author.split()
                if len(parts) >= 2:
                    last_name = parts[-1]
                    first_initial = parts[0][0]
                    authors.append(f"{last_name}, {first_initial}.")
                else:
                    authors.append(author)

        # Join authors with commas and "and" for the last author
        if len(authors) > 1:
            authors_text = ", ".join(authors[:-1]) + ", & " + authors[-1]
        else:
            authors_text = authors[0] if authors else ""

        citation = ""
        if pub_type == "article":
            # Format for journal articles: Author(s). (Year). Title. Journal, Volume(Number), Pages.
            citation = f"{authors_text} ({pub['year']}). {pub['title']}. "

            if 'journal' in pub:
                citation += f"*{pub['journal']}*"

                if 'volume' in pub:
                    citation += f", {pub['volume']}"

                if 'number' in pub:
                    citation += f"({pub['number']})"

                if 'pages' in pub and pub['pages']:
                    citation += f", {pub['pages']}"

                citation += "."

                if 'publisher' in pub and pub['publisher']:
                    citation += f" {pub['publisher']}."
            else:
                # For articles without a journal specified
                citation += "."

        elif pub_type == "inproceedings":
            # Format for conference proceedings: Author(s). (Year). Title. In Proceedings, Pages.
            citation = f"{authors_text} ({pub['year']}). {pub['title']}. "

            if 'booktitle' in pub:
                citation += f"In *{pub['booktitle']}*"

                if 'pages' in pub and pub['pages']:
                    citation += f", pp. {pub['pages']}"

                citation += "."

                if 'organization' in pub and pub['organization']:
                    citation += f" {pub['organization']}."
            else:
                citation += "."

        elif pub_type == "inbook":
            # Format for book chapters: Author(s). (Year). Title. In Book Title, Pages.
            citation = f"{authors_text} ({pub['year']}). {pub['title']}. "

            if 'booktitle' in pub:
                citation += f"In *{pub['booktitle']}*"

                if 'pages' in pub and pub['pages']:
                    citation += f", pp. {pub['pages']}"

                citation += "."

                if 'note' in pub and pub['note']:
                    citation += f" {pub['note']}."
            else:
                citation += "."

        # Add citation count if available
        if 'citations' in pub and pub['citations'] > 0:
            citation += f" (Cited {pub['citations']} times)"

        md += f"- {citation}\n"

    return md


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a Markdown file with pymd blocks.')
    parser.add_argument('file_path', type=str, help='Path to the Markdown file')
    args = parser.parse_args()

    processed_content = process_markdown(args.file_path)
    print(processed_content)
