from fastapi import Request
from fastapi_users import BaseUserManager, IntegerIDMixin
import logging
from typing import TYPE_CHECKING, Optional
from mailing.send_email_confirmed import send_email_confirmed
from fastapi_users.db import BaseUserDatabase

from core.models import User
from mailing.send_forgot_password_email import send_forgot_password_email
from mailing.send_password_changed_email import send_password_changed_email
from mailing.send_verification_email import send_verification_email
from ..config import settings

log = logging.getLogger(__name__)

if TYPE_CHECKING:
    from fastapi import Request



class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret
    def __init__(
            self,
            user_db: BaseUserDatabase[User, int],
            password_helper: Optional["PasswordHelperProtocol"] = None,
            background_tasks: Optional["BackgroundTasks"] = None,
    ):
        super().__init__(user_db, password_helper)
        self.background_tasks = background_tasks

    async def on_after_register(self, user: User, request: Request | None = None):
        log.warning(
            "User %r has registered.",
            user.id,
        )

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ):
        log.warning(
            "Verification requested for user %r. Verification token: %r",
            user.id,
            token,
        )
        verification_link = request.url_for("verify-email").replace_query_params(
            token=token
        )
        self.background_tasks.add_task(
            send_verification_email,
            user=user,
            verification_link=str(verification_link),
            verification_token=token,
        )

    async def on_after_verify(
            self,
            user: User,
            request: Optional["Request"] = None,
    ):
        log.warning(
            "User %r has been verified",
            user.id,
        )
        self.background_tasks.add_task(
            send_email_confirmed,
            user=user,
        )


    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ):
        log.warning(
            "User %r has forgot their password. Reset token: %r",
            user.id,
            token,
        )
        reset_link = request.url_for("reset-password").replace_query_params(
            token=token
        )

        self.background_tasks.add_task(
            send_forgot_password_email,  # Твоя новая функция
            user=user,
            token=token,
            reset_link=reset_link,
        )

    async def on_after_reset_password(
            self, user: User, request: Request | None = None
    ):
        log.warning("User %r has successfully reset their password", user.id)

        self.background_tasks.add_task(
            send_password_changed_email,
            user=user,
        )



