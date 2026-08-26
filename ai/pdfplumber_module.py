import pdfplumber


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a text-based PDF using pdfplumber."""
    chunks = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                chunks.append(page_text)
    return "\n".join(chunks).strip()
