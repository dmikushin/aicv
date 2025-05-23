"""
Custom Markdown extensions for the AI-aware CV generator
"""
import sys
import io
import re
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from aicv.renderers import render
from aicv.backend.html import EmojisFormatterHtml
from aicv.backend.markdown import EmojisFormatterMarkdown
from aicv.backend.moderncv import EmojisFormatterModernCV
from aicv.utils.escape_latex import escape_latex

class PyMdExtension(Extension):
    """A custom Markdown extension to handle `pymd` blocks."""
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.register(PyMdPreprocessor(md), 'pymd', 175)


class PyMdPreprocessor(Preprocessor):
    """A preprocessor that identifies `pymd` blocks, executes the Python code within them, and replaces the block with the result."""
    def __init__(self, personal_info, backend='markdown', emojis=True):
        super().__init__(None)
        self.personal_info = personal_info
        self.backend = backend
        self.emojis = emojis

    def run(self, lines):
        new_lines = []
        pymd_block = False
        pymd_code = []
        md_buffer = []

        import markdown as _markdown
        md_converter = None
        if self.backend == 'html':
            md_converter = _markdown.Markdown(extensions=[])

        for line in lines:
            if line.strip().startswith('```pymd'):
                # Flush markdown buffer before entering pymd block
                if self.backend == 'html' and md_buffer:
                    html = md_converter.convert('\n'.join(md_buffer))
                    if self.emojis:
                        html = EmojisFormatterHtml.add_section_emojis(html)
                    new_lines.extend(html.splitlines())
                    md_buffer = []
                elif self.backend == 'markdown' and md_buffer:
                    md_content = '\n'.join(md_buffer)
                    if self.emojis:
                        md_content = EmojisFormatterMarkdown.add_section_emojis(md_content)
                    new_lines.extend(md_content.splitlines())
                    md_buffer = []
                elif self.backend == 'moderncv' and md_buffer:
                    latex_content = self._convert_markdown_to_latex('\n'.join(md_buffer))
                    if self.emojis:
                        latex_content = EmojisFormatterModernCV.add_section_emojis(latex_content)
                    new_lines.extend(latex_content.splitlines())
                    md_buffer = []
                pymd_block = True
                pymd_code = []
            elif line.strip() == '```' and pymd_block:
                pymd_block = False
                # Redirect stdout to capture the output of the executed code
                old_stdout = sys.stdout
                sys.stdout = io.StringIO()
                try:
                    def render_with_backend(json_filename, backend=self.backend):
                        from aicv.renderers import render as real_render
                        return real_render(json_filename, backend, emojis=self.emojis)
                    exec('\n'.join(pymd_code), {**globals(), 'render': render_with_backend})
                    output = sys.stdout.getvalue()
                    new_lines.extend(output.splitlines())
                finally:
                    sys.stdout = old_stdout
            elif pymd_block:
                pymd_code.append(line)
            else:
                md_buffer.append(line)

        # Flush any remaining markdown buffer at the end
        if self.backend == 'html' and md_buffer:
            html = md_converter.convert('\n'.join(md_buffer))
            if self.emojis:
                html = EmojisFormatterHtml.add_section_emojis(html)
            new_lines.extend(html.splitlines())
        elif self.backend == 'markdown' and md_buffer:
            md_content = '\n'.join(md_buffer)
            if self.emojis:
                md_content = EmojisFormatterMarkdown.add_section_emojis(md_content)
            new_lines.extend(md_content.splitlines())
        elif self.backend == 'moderncv' and md_buffer:
            latex_content = self._convert_markdown_to_latex('\n'.join(md_buffer))
            if self.emojis:
                latex_content = EmojisFormatterModernCV.add_section_emojis(latex_content)
            new_lines.extend(latex_content.splitlines())

        return new_lines

    def _convert_markdown_to_latex(self, markdown_content):
        """Convert markdown content to LaTeX format suitable for moderncv."""
        lines = markdown_content.strip().split('\n')
        latex_lines = []
        in_list = False

        for line in lines:
            line = line.strip()

            if not line:
                if in_list:
                    latex_lines.append('\\end{itemize}')
                    in_list = False
                latex_lines.append('')
                continue

            # Handle headers
            if line.startswith('## '):
                if in_list:
                    latex_lines.append('\\end{itemize}')
                    in_list = False
                header_text = line[3:].strip()
                latex_lines.append(f'\\section{{{escape_latex(header_text)}}}')

            elif line.startswith('# '):
                if in_list:
                    latex_lines.append('\\end{itemize}')
                    in_list = False
                header_text = line[2:].strip()
                latex_lines.append(f'\\section{{{escape_latex(header_text)}}}')

            elif line.startswith('### '):
                if in_list:
                    latex_lines.append('\\end{itemize}')
                    in_list = False
                header_text = line[4:].strip()
                latex_lines.append(f'\\subsection{{{escape_latex(header_text)}}}')

            # Handle list items
            elif line.startswith('- '):
                if not in_list:
                    latex_lines.append('\\begin{itemize}')
                    in_list = True
                item_text = line[2:].strip()
                # Convert markdown formatting in list items
                item_text = self._convert_markdown_formatting(item_text)
                latex_lines.append(f'\\item {item_text}')

            # Handle regular paragraphs
            else:
                if in_list:
                    latex_lines.append('\\end{itemize}')
                    in_list = False
                # Convert markdown formatting in paragraphs
                paragraph_text = self._convert_markdown_formatting(line)
                if paragraph_text:
                    latex_lines.append(f'{paragraph_text}')

        # Close any remaining list
        if in_list:
            latex_lines.append('\\end{itemize}')

        return '\n'.join(latex_lines)

    def _convert_markdown_formatting(self, text):
        """Convert markdown formatting (bold, italic, etc.) to LaTeX."""
        # Handle bold text - extract content, escape it, then wrap in \textbf
        def replace_bold(match):
            content = match.group(1)
            escaped_content = escape_latex(content)
            return f'\\textbf{{{escaped_content}}}'
        text = re.sub(r'\*\*(.*?)\*\*', replace_bold, text)

        # Handle italic text - extract content, escape it, then wrap in \textit
        def replace_italic(match):
            content = match.group(1)
            escaped_content = escape_latex(content)
            return f'\\textit{{{escaped_content}}}'
        text = re.sub(r'\*(.*?)\*', replace_italic, text)

        # Handle inline code - extract content, escape it, then wrap in \texttt
        def replace_code(match):
            content = match.group(1)
            escaped_content = escape_latex(content)
            return f'\\texttt{{{escaped_content}}}'
        text = re.sub(r'`(.*?)`', replace_code, text)

        # Escape any remaining LaTeX special characters in the rest of the text
        # We need to be careful not to escape the LaTeX commands we just added
        parts = []
        last_end = 0

        # Find all LaTeX commands we just inserted
        latex_commands = list(re.finditer(r'\\(?:textbf|textit|texttt)\{[^}]*\}', text))

        for match in latex_commands:
            # Escape the text before this LaTeX command
            before_text = text[last_end:match.start()]
            if before_text:
                parts.append(escape_latex(before_text))
            # Keep the LaTeX command as-is
            parts.append(match.group())
            last_end = match.end()

        # Escape any remaining text after the last LaTeX command
        remaining_text = text[last_end:]
        if remaining_text:
            parts.append(escape_latex(remaining_text))

        return ''.join(parts)
