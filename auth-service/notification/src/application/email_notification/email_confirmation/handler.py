from dataclasses import dataclass

from src.application.email_notification.smtp_service import SmtpService
from src.config import ApiPathsConfig


@dataclass
class EmailConfirmationCommand:
    email: str
    email_confirmation_token: str


class EmailConfirmationHandler:
    def __init__(self, smtp_service: SmtpService, api_paths_conf: ApiPathsConfig):
        self.smtp_service = smtp_service
        self.api_paths_conf = api_paths_conf

    async def handle(self, command: EmailConfirmationCommand):
        rendered_url = f"{self.api_paths_conf.backend_url}{self.api_paths_conf.email_confirmation_url.replace("{code}", command.email_confirmation_token)}"
        body = f"""
        Здравствуйте! Если вы зарегистрировались в приложении task tracker,
        используя эту почту, то перейдите по следующей ссылке:
        {rendered_url}
        чтобы подтвердить регистрацию."""
        await self.smtp_service.send_email(command.email, "Подтверждение почты", body)
