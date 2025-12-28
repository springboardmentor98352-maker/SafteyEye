import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email_alert(receiver_email, subject, body, attachment_path=None, sender_email=None, app_password=None):
    if not sender_email or not app_password:
        return False, "⚠ Missing sender email or app password."
    if not receiver_email:
        return False, "⚠ Missing receiver email."

    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        if attachment_path and os.path.exists(attachment_path):
            filename = os.path.basename(attachment_path)
            with open(attachment_path,"rb") as f:
                part = MIMEBase("application","octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition",f"attachment; filename={filename}")
            msg.attach(part)

        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        return True, "✅ Email sent successfully!"
    except Exception as e:
        return False, f"❌ SMTP Error: {e}"
