import os
import pytesseract
from PIL import Image


def extract_text_from_image(image_path: str) -> str:
    """Extract text from an image using Tesseract OCR."""
    lang = os.getenv("OCR_LANG", "eng").strip() or "eng"
    try:
        with Image.open(image_path) as img:
            text = pytesseract.image_to_string(img, lang=lang)
    except pytesseract.TesseractNotFoundError as exc:
        raise RuntimeError(
            "Tesseract OCR is not installed/configured on this machine. "
            "Install Tesseract and ensure its executable is on PATH."
        ) from exc
    return text.strip()
