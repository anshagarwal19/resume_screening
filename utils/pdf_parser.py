import fitz


def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract text from uploaded PDF resume.
    """

    pdf_bytes = pdf_file.read()

    document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text.strip()