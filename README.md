# AI-aware Curriculum Citae

Get your AI-managed CV!

## Usage

1. Prepare `cv.md` file with your main CV content.

2. Place your photo into `photo.jpg` (case-sensitive) file in the current folder or next to the `cv.md` file.

3. Put your employment history, education, and peer-reviewed publications into `employment.json`, `education.json`, and `publications.json`, respectively, in the current folder or next to the `cv.md` file.

4. Execute the CV generation script:

```
aicv example/cv.md
```

## Format Options

### HTML Generation (Default)

By default, `aicv` generates an HTML version of your CV:

```
aicv example/cv.md
```

### PDF Export

You can generate a PDF version of your CV with proper A4 paper size and page numbering:

```
aicv example/cv.md --pdf
```

This will create only the PDF version of your CV (no HTML file will be generated).

#### PDF Options

- `--pdf`: Generate only a PDF version of your CV (no HTML file)
- `--pdf-output PATH`: Specify a custom output path for the PDF file
- `--paper SIZE`: Set a custom paper size (default: A4)
- `--no-page-numbers`: Disable page numbers in the PDF output

Example with custom PDF path:

```
aicv example/cv.md --pdf --pdf-output my_professional_cv.pdf
```

### Markdown Export

You can generate a clean, intermediate Markdown representation of your CV that can be easily parsed by LLMs for further processing:

```
aicv example/cv.md --markdown processed_cv.md
```

This will generate only the Markdown representation with all pymd blocks executed and skip any HTML/PDF generation.

### Installing PDF Support

PDF support requires the WeasyPrint library. To install it:

```
pip install weasyprint
```

Or when installing the package:

```
pip install aicv[pdf]
```

For more details on WeasyPrint installation requirements, see the [WeasyPrint Documentation](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation).