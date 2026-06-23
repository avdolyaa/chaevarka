from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiosmtplib
from core.config import settings

async def send_email(
    recipient: str,
    subject: str,
    plain_content: str,
    html_content: str = "",
):
    admin_email = settings.smtp.from_email
    message = MIMEMultipart("alternative")
    message["From"] = settings.smtp.from_email
    message["To"] = recipient
    message["Subject"] = subject

    plain_text_message = MIMEText(
        plain_content,
        "plain",
        "utf-8"
    )
    message.attach(plain_text_message)
    if html_content:
        html_message = MIMEText(
            html_content,
            "html",
            "utf-8"
        )
        message.attach(html_message)
    await aiosmtplib.send(
        message,
        hostname=settings.smtp.host,
        port=settings.smtp.port,
        username=settings.smtp.username or None,
        password=settings.smtp.password or None,
        use_tls=settings.smtp.use_tls,
    )