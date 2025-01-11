import logging
import os

from dishka.integrations.base import FromDishka
from faststream.nats import NatsRouter

from src.application.email_notification.email_confirmation.handler import EmailConfirmationHandler, \
    EmailConfirmationCommand
from src.application.email_notification.reset_password.handler import ResetPasswordCommand, ResetPasswordHandler

email_router = NatsRouter()

# class EmailConfirmationSchema(BaseModel):
#     email: EmailStr
#     email_confirmation_token: str

# @nats_router.subscriber("email.reset_password")


logger = logging.getLogger(__name__)


@email_router.subscriber(os.getenv("EMAIL_CONFIRMATION_SUB", "email.confirmation"))
async def handle_email_confirmation(command: EmailConfirmationCommand, handler: FromDishka[EmailConfirmationHandler]) -> None:
    logger.info(f"Received command: {command}")
    await handler.handle(command)


@email_router.subscriber(os.getenv("EMAIL_RESET_PWD_SUB", "email.reset_password"))
async def handle_email_reset_pwd(command: ResetPasswordCommand, handler: FromDishka[ResetPasswordHandler]) -> None:
    await handler.handle(command)
