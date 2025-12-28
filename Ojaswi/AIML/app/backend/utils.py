import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_pdf(vid, label, image_path, timestamp, confidence):
    os.makedirs("database", exist_ok=True)
    pdf_path = f"database/{vid}.pdf"
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "🚨 PPE Violation Challan")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Violation ID: {vid}")
    c.drawString(50, height - 130, f"Violation Type: {label}")
    c.drawString(50, height - 160, f"Confidence: {confidence:.2f}")
    c.drawString(50, height - 190, f"Timestamp: {timestamp}")

    if os.path.exists(image_path):
        c.drawImage(image_path, 50, height - 520, width=400, preserveAspectRatio=True)

    c.showPage()
    c.save()
    return pdf_path
