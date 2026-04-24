import smtplib
from email.message import EmailMessage


def send_secret_key_email(*, recipient, name, secret_key, app_config):
    email_user = app_config.get("MAIL_USERNAME")
    email_pass = app_config.get("MAIL_PASSWORD")

    if not email_user or not email_pass:
        return {
            "sent": False,
            "reason": "EMAIL_USER and EMAIL_PASS are not configured. Secret key delivery skipped.",
        }

    message = EmailMessage()
    message["Subject"] = "QuantumPay Secure Key"
    message["From"] = email_user
    message["To"] = recipient
    message.set_content(
        f"Hello {name},\n\n"
        f"Your Secret Key:\n{secret_key}\n\n"
        "Do NOT share this key.\n"
    )

    try:
        with smtplib.SMTP(app_config.get("MAIL_SERVER"), app_config.get("MAIL_PORT")) as server:
            if app_config.get("MAIL_USE_TLS"):
                server.starttls()
            server.login(email_user, email_pass)
            server.send_message(message)
        return {"sent": True, "reason": "Secret key emailed successfully."}
    except Exception as exc:
        return {"sent": False, "reason": f"Failed to send email: {exc}"}
