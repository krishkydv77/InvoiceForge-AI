# AI Invoice Generator

AI-powered invoice processing API built with FastAPI, MySQL, document parsers, Gemini, validation and PDF generation.

## Features

- Upload PDF, image, DOCX, XLSX or CSV invoices.
- Extract invoice text using document parsers/OCR.
- Extract structured invoice fields with Gemini.
- Validate totals and invoice fields with deterministic Python rules.
- Generate a masked invoice PDF.
- Store invoice metadata in MySQL.
- Direct invoice creation endpoint for testing without Gemini.

## Project Structure

```text
invoce/
├── ai/
├── routers/
├── services/
├── utils/
├── templates/
├── invoices/
├── uploads/
├── config.py
├── database.py
├── models.py
├── main.py
├── requirements.txt
└── .env
```

## 1. Create MySQL Database

```sql
CREATE DATABASE invoice_db;
```

Then edit `.env`:

```env
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/invoice_db
GEMINI_API_KEY=
OCR_LANG=eng
```

Keep the API key empty until you are ready to use the upload/AI endpoint.

## 2. Create Virtual Environment

Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## 3. Run API

From the `invoce` directory:

```powershell
uvicorn main:app --reload
```

Open:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/docs`

## 4. Test Without Gemini API

Use:

```text
POST /api/invoice/direct
```

It accepts form fields:

- `customer_name`
- `mobile`
- `address`
- `items` — JSON array such as `[{"name":"Product A","quantity":2,"price":100}]`
- `tax`
- `due_date` — `YYYY-MM-DD`

This endpoint does not call Gemini.

## 5. Enable Gemini Later

Add your real key to `.env`:

```env
GEMINI_API_KEY=YOUR_REAL_KEY
```

Then use:

```text
POST /api/invoice/upload
```

## OCR Note

For image invoices, Tesseract OCR must be installed separately on Windows and available on PATH. If Hindi OCR is required, install the Hindi Tesseract language data and set:

```env
OCR_LANG=eng+hin
```

For scanned/image-only PDFs, the project includes a `pdf2image` fallback. Poppler must also be installed and available on PATH.

## Security

Do not commit `.env`, API keys, database passwords, generated invoices or virtual environments to GitHub.
