from datetime import date
from decimal import Decimal, InvalidOperation


def _number(value, field_name: str, errors: list[str], default=None):
    if value is None and default is not None:
        return default
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        errors.append(f"{field_name} must be a valid number")
        return Decimal("0")


def validate_invoice_data(data: dict) -> dict:
    errors = []
    if not isinstance(data, dict):
        return {"is_valid": False, "errors": ["Invoice data must be a JSON object"], "calculated_total": 0.0}

    items = data.get("items")
    if not isinstance(items, list):
        errors.append("Items must be a list")
        items = []

    if not data.get("customer_name"):
        errors.append("Customer name missing")
    if not data.get("mobile"):
        errors.append("Mobile number missing")
    if not items:
        errors.append("No items found")

    subtotal = Decimal("0")
    normalized_items = []
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            errors.append(f"Item {index} must be an object")
            continue
        if not item.get("name"):
            errors.append(f"Item {index} name missing")
        quantity = _number(item.get("quantity"), f"Item {index} quantity", errors)
        price = _number(item.get("price"), f"Item {index} price", errors)
        if quantity < 0:
            errors.append(f"Item {index} quantity cannot be negative")
        if price < 0:
            errors.append(f"Item {index} price cannot be negative")
        subtotal += quantity * price
        normalized_items.append({
            "name": item.get("name", ""),
            "quantity": float(quantity),
            "price": float(price),
        })

    tax = _number(data.get("tax"), "Tax", errors, default=Decimal("0"))
    total = _number(data.get("total"), "Total", errors)
    calculated_total = subtotal + tax

    if abs(calculated_total - total) > Decimal("0.01"):
        errors.append(f"Total mismatch. Expected {calculated_total}, got {data.get('total')}")

    due_date = data.get("due_date")
    if due_date:
        try:
            date.fromisoformat(str(due_date))
        except ValueError:
            errors.append("Due date must use YYYY-MM-DD format")

    return {
        "is_valid": not errors,
        "errors": errors,
        "calculated_total": float(calculated_total),
        "normalized_items": normalized_items,
    }
