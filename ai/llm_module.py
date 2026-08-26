import json
from config import GEMINI_API_KEY

MODEL_NAME = "gemini-3.6-flash"
_client = None


def _get_client():
    global _client
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. Add your Gemini API key to .env to use /api/invoice/upload."
        )
    if _client is None:
        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError(
                "google-genai is not installed. Run: pip install google-genai"
            ) from exc
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


def _extract_json(text: str) -> dict:
    """Parse JSON even if the model accidentally wraps it in markdown fences/text."""
    cleaned = (text or "").strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start >= 0 and end > start:
            return json.loads(cleaned[start : end + 1])
        raise ValueError("Gemini did not return valid JSON invoice data.")


def extract_invoice_data(text: str) -> dict:
    client = _get_client()
    prompt = f"""
Extract invoice information from the following document text.
Return ONLY a valid JSON object. Do not use markdown fences or explanatory text.
Use exactly these keys:
customer_name, mobile, address, items, tax, total, due_date

items must be an array of objects with exactly: name, quantity, price.
quantity, price, tax and total must be numbers.
If a value is not available, use null (and items should be []).

Document text:
{text}
"""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={"response_mime_type": "application/json"},
    )
    return _extract_json(response.text)


def validate_invoice_data(invoice_data: dict) -> str:
    client = _get_client()
    payload = json.dumps(invoice_data, ensure_ascii=False)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=(
            "Validate this invoice data. Check item arithmetic, tax and total consistency. "
            "Return a concise validation result.\n\n" + payload
        ),
    )
    return response.text or "No AI validation response returned."
