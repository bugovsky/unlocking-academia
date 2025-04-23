from email.mime.text import MIMEText

import aiosmtplib

from backend.utils.config.smtp import smtp_settings


async def send_email(to_email: str, subject: str, body: str) -> None:
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = smtp_settings.sender
    msg["To"] = to_email

    await aiosmtplib.send(
        msg,
        hostname=smtp_settings.smtp_host,
        port=smtp_settings.smtp_port,
        username=smtp_settings.smtp_username,
        password=smtp_settings.smtp_password,
        start_tls=True,
        timeout=15,
    )