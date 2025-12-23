import smtplib
from email.message import EmailMessage

def send_email_alert(violations):
    msg = EmailMessage()
    msg.set_content(
        f"Safety Violation Detected:\n\n{violations}\n\nPlease take immediate action."
    )

    msg["Subject"] = "🚨 SafetyEye Alert - PPE Violation"
    msg["From"] = "sanmayaik02@gmail.com"
    msg["To"] = "madhuraibhat@gmail.com"

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("sanmayaik02@gmail.com", "tbsy iwde kmkb edek")
    server.send_message(msg)
    server.quit()
