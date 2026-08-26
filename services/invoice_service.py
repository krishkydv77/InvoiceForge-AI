import json
import os
import tempfile
from datetime import date

from fastapi import HTTPException

from utils.file_parser import parse_pdf, parse_image, parse_docx, parse_excel, parse_csv
from ai.llm_module import extract_invoice_data, validate_invoice_data as ai_validate_invoice_data
from utils.validators import validate_invoice_data as local_validate
from utils.pdf_generator import generate_masked_invoice
from database import SessionLocal
from models import Invoice

SUPPORTED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".docx", ".xlsx", ".xls", ".csv"}


def _parse_due_date(value):
    if not value:
        return None
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="due_date must use YYYY-MM-DD format") from exc


def _validate_or_raise(data: dict):
    validation = local_validate(data)
    if not validation["is_valid"]:
        raise HTTPException(status_code=422, detail={"message": "Invoice validation failed", "errors": validation["errors"]})
    return validation


def _save_invoice(data: dict, unique_id: str):
    db = SessionLocal()
    try:
        invoice = Invoice(
            unique_id=unique_id,
            customer_name=data.get("customer_name"),
            mobile=data.get("mobile"),
            address=data.get("address"),
            items=json.dumps(data.get("items", []), ensure_ascii=False),
            total=float(data.get("total", 0)),
            tax=float(data.get("tax", 0)),
            due_date=_parse_due_date(data.get("due_date")),
        )
        db.add(invoice)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


async def process_invoice(file):
    filename = (file.filename or "").lower()
    extension = os.path.splitext(filename)[1]
    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {extension or 'unknown'}")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        if extension == ".pdf":
            text = parse_pdf(tmp_path)
        elif extension in {".png", ".jpg", ".jpeg"}:
            text = parse_image(tmp_path)
        elif extension == ".docx":
            text = parse_docx(tmp_path)
        elif extension in {".xlsx", ".xls"}:
            if extension == ".xls":
                raise HTTPException(status_code=400, detail="Legacy .xls is not supported. Convert it to .xlsx first.")
            text = parse_excel(tmp_path)
        else:
            text = parse_csv(tmp_path)

        if not text.strip():
            raise HTTPException(status_code=422, detail="No readable text could be extracted from the uploaded file")

        extracted = extract_invoice_data(text)
        if not isinstance(extracted, dict):
            raise HTTPException(status_code=502, detail="Gemini returned an invalid invoice structure")

        validated_local = _validate_or_raise(extracted)
        validated_ai = ai_validate_invoice_data(extracted)

        unique_id, pdf_path = generate_masked_invoice(extracted)
        _save_invoice(extracted, unique_id)

        return {
            "unique_id": unique_id,
            "pdf_path": pdf_path,
            "validation_ai": validated_ai,
            "validation_local": validated_local,
        }
    except HTTPException:
        raise
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Invoice processing failed: {exc}") from exc
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


async def process_direct_input(payload: dict):
    """Process a directly supplied invoice JSON payload."""
    try:
        items_json = payload.get("items", [])
        items_json = [item if isinstance(item, dict) else item.model_dump() for item in items_json]

        tax_value = float(payload.get("tax", 0))
        subtotal = sum(float(item["quantity"]) * float(item["price"]) for item in items_json)
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=422,
            detail="Each item must contain numeric quantity and price",
        ) from exc

    data = {
        "customer_name": payload.get("customer_name"),
        "mobile": payload.get("mobile"),
        "address": payload.get("address"),
        "items": items_json,
        "tax": tax_value,
        "total": subtotal + tax_value,
        "due_date": payload.get("due_date"),
    }

    validated_local = _validate_or_raise(data)
    unique_id, pdf_path = generate_masked_invoice(data)
    _save_invoice(data, unique_id)

    return {
        "unique_id": unique_id,
        "pdf_path": pdf_path,
        "validation_local": validated_local,
    }
