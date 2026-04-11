from textwrap import dedent
from core.models import User
from jinja_templates import templates
from mailing.send_email import send_email


async def send_password_changed_email(
    user: User,
):
    recipient = user.email
    subject = "Password Successfully Changed"

    plain_content = dedent(
        f"""\
        Dear {user.first_name or recipient},

        This is a confirmation that your password has been successfully changed.
        If you did NOT perform this action, please contact support immediately.

        Your site admin,
        © 2026.
        """
    )

    template = templates.get_template("mailing/password-reset/forgot-password-request.html")
    context = {
        "user": user,
    }
    html_content = template.render(context)

    await send_email(
        recipient=recipient,
        subject=subject,
        plain_content=plain_content,
        html_content=html_content,
    )