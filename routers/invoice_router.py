from datetime import date

from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel, Field

from services.invoice_service import process_invoice, process_direct_input

router = APIRouter()


class InvoiceItem(BaseModel):
    name: str = Field(..., min_length=1, description="Product or service name")
    quantity: float = Field(..., ge=0, description="Quantity")
    price: float = Field(..., ge=0, description="Unit price")


class DirectInvoiceRequest(BaseModel):
    customer_name: str = Field(..., min_length=1)
    mobile: str = Field(..., min_length=1)
    address: str = Field(..., min_length=1)
    items: list[InvoiceItem] = Field(..., min_length=1)
    tax: float = Field(..., ge=0)
    due_date: date


@router.post("/invoice/upload")
async def upload_invoice(file: UploadFile = File(...)):
    return await process_invoice(file)


@router.post("/invoice/direct")
async def direct_invoice(payload: DirectInvoiceRequest):
    return await process_direct_input(payload.model_dump())
