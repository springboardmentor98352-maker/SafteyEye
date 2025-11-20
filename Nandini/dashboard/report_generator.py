from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_pdf(total_alerts, compliance):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    c.drawString(50, 750, "SafetyEye – Daily Safety Report")
    c.drawString(50, 720, f"Total Alerts: {total_alerts}")
    c.drawString(50, 700, f"Compliance: {compliance}%")

    c.drawString(50, 660, "Insights:")
    c.drawString(70, 640, "- Helmet Missing is the top violation.")
    c.drawString(70, 620, "- Alerts peak during afternoon hours.")

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer
