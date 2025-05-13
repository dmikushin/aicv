"""
Custom Markdown extensions for the AI-aware CV generator
"""
import sys
import io
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from aicv.renderers import render

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
                    new_lines.extend(html.splitlines())
                    md_buffer = []
                elif self.backend == 'markdown' and md_buffer:
                    new_lines.extend(md_buffer)
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
            new_lines.extend(html.splitlines())
        elif self.backend == 'markdown' and md_buffer:
            new_lines.extend(md_buffer)

        return new_lines
