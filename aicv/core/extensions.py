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
