from pathlib import Path
import uuid

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from config import BASE_DIR, INVOICES_DIR, TEMPLATES_DIR


def generate_masked_invoice(data: dict, template_dir: str | Path | None = None):
    template_path = Path(template_dir) if template_dir else TEMPLATES_DIR
    if not template_path.is_absolute():
        template_path = BASE_DIR / template_path
    if not template_path.exists():
        raise FileNotFoundError(f"Invoice template directory not found: {template_path}")

    INVOICES_DIR.mkdir(parents=True, exist_ok=True)
    env = Environment(loader=FileSystemLoader(str(template_path)))
    template = env.get_template("invoice_template.html")

    unique_id = str(uuid.uuid4())[:8]
    masked_data = dict(data)
    masked_data["unique_id"] = unique_id
    masked_data["customer_name"] = "XXXX"
    masked_data["mobile"] = "XXXXXX"
    masked_data["address"] = "XXXXXX"

    html_out = template.render(data=masked_data)
    pdf_file = INVOICES_DIR / f"invoice_{unique_id}.pdf"
    HTML(string=html_out, base_url=str(BASE_DIR)).write_pdf(str(pdf_file))

    return unique_id, str(pdf_file)
