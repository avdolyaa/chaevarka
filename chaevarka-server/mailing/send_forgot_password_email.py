from textwrap import dedent
from core.models import User
from jinja_templates import templates
from mailing.send_email import send_email


async def send_forgot_password_email(
        user: User,
        token: str,
        reset_link: str,
):
    recipient = user.email
    subject = "Password Reset Request"

    plain_content = dedent(
        f"""\
        Dear {user.first_name or recipient},

        Someone requested a password reset for your account. 
        If this was you, please follow the link and use the token below:

        Link: {reset_link}
        Token: {token}

        If you didn't request this, please ignore this email.

        Your site admin,
        © 2026.
        """
    )

    template = templates.get_template("mailing/password-reset/forgot-password.html")
    context = {
        "user": user,
        "reset_link": reset_link,
        "token": token,
    }
    html_content = template.render(context)

    await send_email(
        recipient=recipient,
        subject=subject,
        plain_content=plain_content,
        html_content=html_content,
    )