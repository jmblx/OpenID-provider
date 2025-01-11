from dataclasses import dataclass

from pydantic import BaseModel

from src.application.email_notification.smtp_service import SmtpService
from src.config import ApiPathsConfig

@dataclass
class ResetPasswordCommand:
    email: str
    reset_password_token: str

class ResetPasswordHandler:
    def __init__(self, smtp_service: SmtpService, api_paths_conf: ApiPathsConfig):
        self.smtp_service = smtp_service
        self.api_paths_conf = api_paths_conf

    async def handle(self, command: ResetPasswordCommand):
        rendered_url = f"{self.api_paths_conf.backend_url}{self.api_paths_conf.reset_password_url.replace("{token}", command.reset_password_token)}"
        body = f"""
        Здравствуйте! Кто-то пытается сменить пароль по этой почте,
        вот ссылка, по которой нужно перейти, чтобы сменить пароль:
        {rendered_url}
        длительность ссылки = 15 минут
        если это не вы, то возможно к вашему аккаунту пытаются
        получить доступ злоумышленники."""
        await self.smtp_service.send_email(command.email, "Сброс пароля", body)
