import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
OCR_LANG = os.getenv("OCR_LANG", "eng").strip() or "eng"

TEMPLATES_DIR = BASE_DIR / "templates"
INVOICES_DIR = BASE_DIR / "invoices"
UPLOADS_DIR = BASE_DIR / "uploads"

INVOICES_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
