"""
Publications section renderer for the AI-aware CV generator
"""

def render_publications(publications, backend="markdown"):
    """
    Custom rendering of publications data with our styling and emojis.
    Publications with "to appear" status are displayed first, then sorted by citation count.
    Supports markdown and html backends.
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

    if backend == "html":
        html = '<ul class="publications-list">'
        for pub in sorted_publications:
            pub_type = pub.get('type', 'article')

            # Select emoji based on status and citation count
            is_to_appear = 'note' in pub and pub.get('note') and 'to appear' in pub.get('note', '').lower()

            if is_to_appear:
                citation_emoji = "🔥"  # Fire emoji for upcoming/to appear publications
            else:
                citation_count = pub.get('citations', 0)
                if citation_count > 30:
                    citation_emoji = "🌟"
                elif citation_count > 15:
                    citation_emoji = "⭐"
                elif citation_count > 5:
                    citation_emoji = "📊"
                else:
                    citation_emoji = "📄"

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

            html += f'<li>{citation}</li>'
        html += '</ul>'
        return html
    else:
        md = ""

        # Format each publication according to its type
        for pub in sorted_publications:
            pub_type = pub.get('type', 'article')

            # Select emoji based on status and citation count
            is_to_appear = 'note' in pub and pub.get('note') and 'to appear' in pub.get('note', '').lower()

            if is_to_appear:
                citation_emoji = "🔥"  # Fire emoji for upcoming/to appear publications
            else:
                citation_count = pub.get('citations', 0)
                if citation_count > 30:
                    citation_emoji = "🌟"
                elif citation_count > 15:
                    citation_emoji = "⭐"
                elif citation_count > 5:
                    citation_emoji = "📊"
                else:
                    citation_emoji = "📄"

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

            md += f"- {citation}\n"

        return md
