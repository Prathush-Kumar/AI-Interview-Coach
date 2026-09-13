import pymupdf


def extract_resume_text(pdf_bytes):
    """
    Extract text from an uploaded PDF resume.
    """

    document = pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    resume_text = ""

    for page in document:
        resume_text += page.get_text()

    document.close()

    return resume_text.strip()