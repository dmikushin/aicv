"""
Publications section renderer for the AI-aware CV generator
"""
from aicv.utils.escape_latex import escape_latex

def render_publications(publications, backend="markdown", emojis=True):
    """
    Custom rendering of publications data with our styling and emojis.
    Publications with "to appear" status are displayed first, then sorted by citation count.
    Supports markdown, html, and moderncv backends.
    """
    # First identify "to appear" publications
    to_appear_publications = []
    regular_publications = []

    for pub in publications:
        # Check if it's a "to appear" publication (either in the note field or in the title/abstract)
        is_to_appear = False
        if 'note' in pub and pub.get('note') and 'to appear' in pub.get('note', '').lower():
            is_to_appear = True

        if is_to_appear:
            to_appear_publications.append(pub)
        else:
            regular_publications.append(pub)

    # Sort regular publications by citation count in descending order
    sorted_regular_publications = sorted(regular_publications, key=lambda pub: pub.get('citations', 0), reverse=True)

    # Sort "to appear" publications by year (most recent first)
    sorted_to_appear_publications = sorted(to_appear_publications, key=lambda pub: pub.get('year', 0), reverse=True)

    # Combine the two lists: "to appear" publications first, then regular publications
    sorted_publications = sorted_to_appear_publications + sorted_regular_publications

    def get_emoji(is_to_appear, citation_count):
        if not emojis:
            return ''
        if is_to_appear:
            return "🔥"
        if citation_count > 30:
            return "🌟"
        elif citation_count > 15:
            return "⭐"
        elif citation_count > 5:
            return "📊"
        else:
            return "📄"

    if backend == "html":
        html = '<ul class="publications-list">'
        for pub in sorted_publications:
            pub_type = pub.get('type', 'article')

            # Select emoji based on status and citation count
            is_to_appear = 'note' in pub and pub.get('note') and 'to appear' in pub.get('note', '').lower()
            citation_count = pub.get('citations', 0)
            citation_emoji = get_emoji(is_to_appear, citation_count)

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
                citation = f"{citation_emoji} {authors_text} ({pub['year']}). {pub['title']}. "

                if 'journal' in pub:
                    citation += f"<em>{pub['journal']}</em>"

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
                citation = f"{citation_emoji} {authors_text} ({pub['year']}). {pub['title']}. "

                if 'booktitle' in pub:
                    citation += f"In <em>{pub['booktitle']}</em>"

                    if 'pages' in pub and pub['pages']:
                        citation += f", pp. {pub['pages']}"

                    citation += "."

                    if 'organization' in pub and pub['organization']:
                        citation += f" {pub['organization']}."
                else:
                    citation += "."

            elif pub_type == "inbook":
                # Format for book chapters: Author(s). (Year). Title. In Book Title, Pages.
                citation = f"{citation_emoji} {authors_text} ({pub['year']}). {pub['title']}. "

                if 'booktitle' in pub:
                    citation += f"In <em>{pub['booktitle']}</em>"

                    if 'pages' in pub and pub['pages']:
                        citation += f", pp. {pub['pages']}"

                    citation += "."

                    if 'note' in pub and pub['note']:
                        citation += f" {pub['note']}."
                else:
                    citation += "."

            elif pub_type == "poster":
                # Format for poster presentations: Author(s). (Year). Title. Poster presented at Conference, Pages.
                citation = f"{citation_emoji} {authors_text} ({pub['year']}). {pub['title']}. "

                if 'booktitle' in pub:
                    citation += f"Poster presented at <em>{pub['booktitle']}</em>"

                    if 'pages' in pub and pub['pages']:
                        citation += f", p. {pub['pages']}"

                    citation += "."

                    if 'note' in pub and pub['note']:
                        citation += f" {pub['note']}."
                else:
                    citation += "."

            # Add citation count if available and it's not a "to appear" publication
            if not is_to_appear and 'citations' in pub and pub['citations'] > 0:
                citation += f" (Cited {pub['citations']} times)"

            citation = citation.replace(citation_emoji + ' ', '') if citation_emoji else citation
            citation = f"{citation_emoji + ' ' if citation_emoji else ''}{citation[len(citation_emoji)+1:] if citation_emoji and citation.startswith(citation_emoji + ' ') else citation}"
            html += f'<li>{citation}</li>'
        html += '</ul>'
        return html

    elif backend == "markdown":
        md = ""

        # Format each publication according to its type
        for pub in sorted_publications:
            pub_type = pub.get('type', 'article')

            # Select emoji based on status and citation count
            is_to_appear = 'note' in pub and pub.get('note') and 'to appear' in pub.get('note', '').lower()
            citation_count = pub.get('citations', 0)
            citation_emoji = get_emoji(is_to_appear, citation_count)

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
                citation = f"{citation_emoji} {authors_text} ({pub['year']}). {pub['title']}. "

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
                citation = f"{citation_emoji} {authors_text} ({pub['year']}). {pub['title']}. "

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
                citation = f"{citation_emoji} {authors_text} ({pub['year']}). {pub['title']}. "

                if 'booktitle' in pub:
                    citation += f"In *{pub['booktitle']}*"

                    if 'pages' in pub and pub['pages']:
                        citation += f", pp. {pub['pages']}"

                    citation += "."

                    if 'note' in pub and pub['note']:
                        citation += f" {pub['note']}."
                else:
                    citation += "."

            elif pub_type == "poster":
                # Format for poster presentations: Author(s). (Year). Title. Poster presented at Conference, Pages.
                citation = f"{citation_emoji} {authors_text} ({pub['year']}). {pub['title']}. "

                if 'booktitle' in pub:
                    citation += f"Poster presented at *{pub['booktitle']}*"

                    if 'pages' in pub and pub['pages']:
                        citation += f", p. {pub['pages']}"

                    citation += "."

                    if 'note' in pub and pub['note']:
                        citation += f" {pub['note']}."
                else:
                    citation += "."

            # Add citation count if available and it's not a "to appear" publication
            if not is_to_appear and 'citations' in pub and pub['citations'] > 0:
                citation += f" (Cited {pub['citations']} times)"

            citation = citation.replace(citation_emoji + ' ', '') if citation_emoji else citation
            citation = f"{citation_emoji + ' ' if citation_emoji else ''}{citation[len(citation_emoji)+1:] if citation_emoji and citation.startswith(citation_emoji + ' ') else citation}"
            md += f"- {citation}\n"

        return md

    elif backend == "moderncv":
        # Generate BibTeX entries and return both LaTeX content and bib content
        bib_entries = []
        citations = []

        for pub in sorted_publications:
            # Generate citation key if not provided
            citation_key = pub.get('citation_key')
            if not citation_key:
                # Generate citation key from first author's last name and year
                first_author = pub['author'][0] if pub['author'] else 'unknown'
                if "," in first_author:
                    last_name = first_author.split(",")[0].strip().lower()
                else:
                    parts = first_author.split()
                    last_name = parts[-1].lower() if parts else 'unknown'
                # Remove non-alphanumeric characters
                last_name = ''.join(c for c in last_name if c.isalnum())
                citation_key = f"{last_name}{pub.get('year', '')}"

            # Store citation key for later reference
            citations.append(citation_key)

            # Generate BibTeX entry
            pub_type = pub.get('type', 'article')

            # Format authors for BibTeX
            authors = []
            for author in pub['author']:
                # Convert to "Last, First" format for BibTeX
                if "," in author:
                    authors.append(author.strip())
                else:
                    # Handle "First Last" format
                    parts = author.split()
                    if len(parts) >= 2:
                        last_name = parts[-1]
                        first_names = " ".join(parts[:-1])
                        authors.append(f"{last_name}, {first_names}")
                    else:
                        authors.append(author)

            authors_str = " and ".join(authors)

            # Build BibTeX entry
            # Note: Don't escape BibTeX content - BibTeX handles special characters itself
            bib_entry = f"@{pub_type}{{{citation_key},\n"
            bib_entry += f"  author = {{{authors_str}}},\n"
            bib_entry += f"  title = {{{pub['title']}}},\n"
            bib_entry += f"  year = {{{pub['year']}}}"

            # Add fields based on publication type
            if pub_type == "article":
                if 'journal' in pub:
                    bib_entry += f",\n  journal = {{{pub['journal']}}}"
                if 'volume' in pub:
                    bib_entry += f",\n  volume = {{{pub['volume']}}}"
                if 'number' in pub:
                    bib_entry += f",\n  number = {{{pub['number']}}}"
                if 'pages' in pub and pub['pages']:
                    bib_entry += f",\n  pages = {{{pub['pages']}}}"
                if 'publisher' in pub and pub['publisher']:
                    bib_entry += f",\n  publisher = {{{pub['publisher']}}}"

            elif pub_type == "inproceedings":
                if 'booktitle' in pub:
                    bib_entry += f",\n  booktitle = {{{pub['booktitle']}}}"
                if 'pages' in pub and pub['pages']:
                    bib_entry += f",\n  pages = {{{pub['pages']}}}"
                if 'organization' in pub and pub['organization']:
                    bib_entry += f",\n  organization = {{{pub['organization']}}}"

            elif pub_type == "inbook":
                if 'booktitle' in pub:
                    bib_entry += f",\n  booktitle = {{{pub['booktitle']}}}"
                if 'pages' in pub and pub['pages']:
                    bib_entry += f",\n  pages = {{{pub['pages']}}}"

            elif pub_type == "poster":
                if 'booktitle' in pub:
                    bib_entry += f",\n  booktitle = {{{pub['booktitle']}}}"
                if 'pages' in pub and pub['pages']:
                    bib_entry += f",\n  pages = {{{pub['pages']}}}"

            # Add note field if present
            if 'note' in pub and pub['note']:
                bib_entry += f",\n  note = {{{pub['note']}}}"

            bib_entry += "\n}\n"
            bib_entries.append(bib_entry)

        # Return both the BibTeX content and citation commands
        bib_content = "\n".join(bib_entries)

        # Generate citation commands for LaTeX
        latex_content = "% Publications are managed via bibliography\n"
        latex_content += "% Use \\nocite{*} to include all references, or \\nocite{key1,key2,...} for specific ones\n"
        if citations:
            latex_content += f"\\nocite{{{','.join(citations)}}}\n"

        # Return tuple of (latex_content, bib_content)
        return (latex_content, bib_content)

    else:
        raise ValueError("Unsupported backend. Use 'html', 'markdown', or 'moderncv'.")
