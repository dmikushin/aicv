"""
LaTeX compilation utilities for the AI-aware CV generator
"""
import os
import subprocess
import shutil

def compile_latex_to_pdf(tex_path: str, output_pdf_path: str, use_bibtex: bool = False, working_directory: str | None = None):
    """
    Compiles a .tex file to .pdf using pdflatex and bibtex (if use_bibtex is True).

    Args:
        tex_path (str): Path to the .tex file.
        output_pdf_path (str): Path for the PDF output.
        use_bibtex (bool): Whether to run bibtex. Defaults to False.
        working_directory (str | None): The directory to run latex commands from. Defaults to tex_path's directory.
    """
    tex_filename = os.path.basename(tex_path)
    base_name = os.path.splitext(tex_filename)[0]
    
    # Determine the directory for compilation processes
    compile_dir = working_directory if working_directory else os.path.dirname(tex_path)
    if not compile_dir: # If tex_path is just a filename, compile_dir might be empty
        compile_dir = '.'

    # Ensure absolute paths for output_pdf_path for clarity, though shutil.move can handle relative.
    # However, pdflatex's -output-directory expects a path where it can write.
    # The final PDF will be in compile_dir/base_name.pdf, then moved.

    # Commands to run, using compile_dir as the execution context for pdflatex output and bibtex processing
    # pdflatex will write its output (aux, log, pdf) to compile_dir.
    # tex_filename should be the simple filename if compile_dir is used as cwd for subprocess, 
    # or an absolute/relative path if not using cwd and relying on -output-directory.
    # For simplicity, let's ensure tex_path is absolute or relative to where this script is run, 
    # and specify output_directory for pdflatex.
    
    # If tex_path is not absolute, make it relative to the original CWD from where the script was called,
    # or assume it's relative to `compile_dir` if `compile_dir` is the intended CWD for subprocesses.
    # Let's assume tex_path is correctly specified (e.g. absolute or relative to the project root)
    # and `compile_dir` is where intermediate files and the initial PDF will be generated.

    pdflatex_cmd = ['pdflatex', '-interaction=nonstopmode', '-output-directory', compile_dir, tex_path]
    # BibTeX runs on the .aux file, which will be in compile_dir
    bibtex_cmd = ['bibtex', os.path.join(compile_dir, base_name)]

    try:
        # First pdflatex pass
        print(f"Running pdflatex (1st pass) on {tex_filename} (output to {compile_dir})...")
        subprocess.run(pdflatex_cmd, check=True, capture_output=True, text=True, cwd=compile_dir)

        if use_bibtex:
            # BibTeX pass
            # Bibtex needs to be run in the directory where the .aux file is.
            print(f"Running bibtex on {base_name}.aux in {compile_dir}...")
            subprocess.run(bibtex_cmd, check=True, capture_output=True, text=True, cwd=compile_dir)

            # Second pdflatex pass (for bibliography)
            print(f"Running pdflatex (2nd pass) on {tex_filename}...")
            subprocess.run(pdflatex_cmd, check=True, capture_output=True, text=True, cwd=compile_dir)

        # Third pdflatex pass (for cross-references and final layout)
        # Some complex documents might need a third pass even without bibtex for other references.
        print(f"Running pdflatex (final pass) on {tex_filename}...")
        subprocess.run(pdflatex_cmd, check=True, capture_output=True, text=True, cwd=compile_dir)

        # The generated PDF will be in compile_dir with name base_name.pdf
        generated_pdf_in_compile_dir = os.path.join(compile_dir, base_name + ".pdf")
        
        if os.path.exists(generated_pdf_in_compile_dir):
            # Ensure the target directory for output_pdf_path exists
            final_output_dir = os.path.dirname(output_pdf_path)
            if final_output_dir and not os.path.exists(final_output_dir):
                os.makedirs(final_output_dir)
            shutil.move(generated_pdf_in_compile_dir, output_pdf_path)
            print(f"PDF successfully generated: {output_pdf_path}")
        else:
            print(f"Error: PDF file {generated_pdf_in_compile_dir} not found after compilation.")
            return

    except subprocess.CalledProcessError as e:
        print(f"Error during LaTeX compilation: {e}")
        print("Stdout:", e.stdout)
        print("Stderr:", e.stderr)
        # Attempt to provide log file content if available
        log_file = os.path.join(compile_dir, base_name + ".log")
        if os.path.exists(log_file):
            print(f"--- Contents of {log_file} ---")
            with open(log_file, 'r', encoding='utf-8') as f_log: # Added encoding
                print(f_log.read())
            print(f"--- End of {log_file} ---")
        blg_file = os.path.join(compile_dir, base_name + ".blg") # BibTeX log
        if use_bibtex and os.path.exists(blg_file):
            print(f"--- Contents of {blg_file} ---")
            with open(blg_file, 'r', encoding='utf-8') as f_blg: # Added encoding
                print(f_blg.read())
            print(f"--- End of {blg_file} ---")
        return
    finally:
        # Clean up auxiliary files from compile_dir
        extensions_to_clean = ['.aux', '.log', '.bbl', '.blg', '.out', '.toc', '.synctex.gz']
        
        for ext in extensions_to_clean:
            aux_file_path = os.path.join(compile_dir, base_name + ext)
            if os.path.exists(aux_file_path):
                try:
                    os.remove(aux_file_path)
                except OSError:
                    print(f"Warning: Could not remove auxiliary file {aux_file_path}")
        # The .tex and .bib files are managed by main.py, so not removed here.
        pass

if __name__ == '__main__':
    # Example usage (requires a sample.tex and sample.bib in a 'temp_compile' directory)
    
    # Create a temporary directory for compilation artifacts
    temp_dir = "temp_latex_compile"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Define file paths relative to the temp_dir
    example_tex_filename = "sample.tex"
    example_bib_filename = "sample.bib"
    example_tex_path = os.path.join(temp_dir, example_tex_filename)
    example_bib_path = os.path.join(temp_dir, example_bib_filename)
    example_output_pdf = os.path.join(temp_dir, "sample_output.pdf")

    sample_tex_content = r"""
\documentclass{article}
\usepackage[backend=bibtex]{biblatex}
\addbibresource{sample.bib}
\title{Sample Document}
\author{Test Author}
\date{\today}
\begin{document}
\maketitle
Hello, world! This is a test document.
\cite{test_entry}.
\printbibliography
\end{document}
"""
    sample_bib_content = r"""
@misc{test_entry,
  author = {Author, Test},
  title = {Test Publication},
  year = {2023}
}
"""
    with open(example_tex_path, "w") as f:
        f.write(sample_tex_content)
    with open(example_bib_path, "w") as f:
        f.write(sample_bib_content)

    print(f"Attempting to compile {example_tex_path} to {example_output_pdf} with bibtex, working in {temp_dir}")
    compile_latex_to_pdf(example_tex_path, example_output_pdf, use_bibtex=True, working_directory=temp_dir)
    
    # Clean up dummy files and directory
    if os.path.exists(example_output_pdf):
         print(f"Successfully created {example_output_pdf}")
    # shutil.rmtree(temp_dir)
    # print(f"Cleaned up temporary directory: {temp_dir}")

    # Test without bibtex
    # os.makedirs(temp_dir, exist_ok=True) # Recreate if removed
    # sample_tex_no_bib_content = sample_tex_content.replace("\\addbibresource{sample.bib}", "").replace("\\cite{test_entry}.", "").replace("\\printbibliography", "")
    # with open(example_tex_path, "w") as f:
    #     f.write(sample_tex_no_bib_content)
    # if os.path.exists(example_bib_path): os.remove(example_bib_path) # Remove bib if it exists for this test
    
    # print(f"\nAttempting to compile {example_tex_path} to {example_output_pdf} WITHOUT bibtex, working in {temp_dir}")
    # compile_latex_to_pdf(example_tex_path, example_output_pdf, use_bibtex=False, working_directory=temp_dir)
    # if os.path.exists(example_output_pdf):
    #      print(f"Successfully created {example_output_pdf} (no bibtex)")
    # shutil.rmtree(temp_dir)
    # print(f"Cleaned up temporary directory: {temp_dir}")

