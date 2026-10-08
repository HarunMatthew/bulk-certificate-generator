from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path


GENERATED_DIR = Path("generated")
GENERATED_DIR.mkdir(exist_ok=True)


def generate_certificate(
    recipient_name: str, event_name: str, event_date: str, certificate_id: int
) -> str:

    filename = f"{certificate_id}_{recipient_name.replace(' ', '_')}.pdf"

    file_path = GENERATED_DIR / filename

    pdf = canvas.Canvas(str(file_path), pagesize=A4)

    width, height = A4

    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(width / 2, height - 180, "CERTIFICATE")

    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(width / 2, height - 250, "This is to certify that")

    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(width / 2, height - 300, recipient_name)

    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(width / 2, height - 360, "has successfully participated in")

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(width / 2, height - 410, event_name)

    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(width / 2, height - 460, f"Date: {event_date}")

    pdf.save()

    return str(file_path)
