"""
core/emailer.py

Small wrapper for sending simple email alerts. This is intentionally minimal.
For Gmail: use App Password (Account -> Security -> App passwords).
DO NOT hardcode credentials in code. Use environment variables.
"""

import smtplib
from email.message import EmailMessage
from typing import List

def send_email_alert(
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
    subject: str,
    body: str,
    to_addrs: List[str],
    use_ssl: bool = True,
) -> bool:
    """
    Send a plain-text email. Returns True if success, False otherwise.
    """
    try:
        msg = EmailMessage()
        msg["From"] = smtp_user
        msg["To"] = ", ".join(to_addrs) if isinstance(to_addrs, (list, tuple)) else to_addrs
        msg["Subject"] = subject
        msg.set_content(body)

        if use_ssl:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=10)
        else:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
            server.ehlo()
            server.starttls()

        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print("Email send failed:", e)
        return False
