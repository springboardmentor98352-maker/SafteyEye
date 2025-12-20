import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def send_email_alert(
        receiver_email,
        subject,
        body,
        attachment_path=None,
        sender_email=None,
        app_password=None
    ):
    """
    Sends an email alert with optional attachment (PDF/Image).

    Returns:
        (success: bool, message: str)
    """

    # -------------------------------
    # Validate Input
    # -------------------------------
    if not sender_email or not app_password:
        return False, "⚠ Missing sender email or app password."

    if not receiver_email:
        return False, "⚠ Missing receiver email."

    # -------------------------------
    # Create Email Structure
    # -------------------------------
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

    except Exception as e:
        return False, f"⚠ Email formatting failed: {e}"

    # -------------------------------
    # Attach PDF / Image File
    # -------------------------------
    if attachment_path:
        try:
            if not os.path.exists(attachment_path):
                return False, f"⚠ Attachment not found: {attachment_path}"

            filename = os.path.basename(attachment_path)

            with open(attachment_path, "rb") as file:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(file.read())

            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={filename}"
            )
            msg.attach(part)

        except Exception as e:
            return False, f"⚠ Failed to attach file: {e}"

    # -------------------------------
    # Send Email using Gmail SMTP
    # -------------------------------
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()

        # Login
        try:
            server.login(sender_email, app_password)
        except Exception as e:
            return False, f"❌ Gmail Login Failed: {e}"

        # Send
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        return True, "✅ Email sent successfully!"

    except Exception as e:
        return False, f"❌ SMTP Error: {e}"
