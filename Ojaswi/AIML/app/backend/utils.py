import cv2
import numpy as np
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import red, black


def read_image(uploaded_file):
    """Convert Streamlit uploaded file into OpenCV image."""
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    return img


def generate_pdf(vid, label, image_path, timestamp, confidence):
    """Generate Police-Style Violation Challan PDF"""

    os.makedirs("database", exist_ok=True)
    pdf_path = f"database/{vid}.pdf"

    try:
        c = canvas.Canvas(pdf_path, pagesize=A4)

        # ---------------- HEADER ----------------
        c.setFont("Helvetica-Bold", 26)
        c.setFillColor(red)
        c.drawString(120, 800, "⚠ TRAFFIC VIOLATION CHALLAN ⚠")

        # Light separator line
        c.setLineWidth(2)
        c.setFillColor(black)
        c.line(50, 785, 545, 785)

        # ---------------- VIOLATION DETAILS ----------------
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 750, "Violation Summary:")

        c.setFont("Helvetica", 12)
        c.drawString(50, 725, f"📌 Violation ID: {vid}")
        c.drawString(50, 705, f"📌 Detected Offense: {label}")
        c.drawString(50, 685, f"📌 Confidence: {confidence:.2f}")
        c.drawString(50, 665, f"📌 Timestamp: {timestamp}")

        # ---------------- IMAGE AREA ----------------
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 630, "Evidence Image:")

        if os.path.exists(image_path):
            c.drawImage(image_path, 50, 410, width=350, height=200)
        else:
            c.setFont("Helvetica-Oblique", 12)
            c.drawString(50, 430, "⚠ Image Missing — Could Not Load Evidence.")

        # ---------------- FOOTER ----------------
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 300, "Officer Signature: _____________________________")

        c.setFont("Helvetica-Oblique", 10)
        c.drawString(50, 270, "This challan was automatically generated using SafetyEye AI Enforcement System.")

        # Save PDF
        c.save()

    except Exception as e:
        print(f"❌ PDF creation failed: {e}")
        return None

    return pdf_path
