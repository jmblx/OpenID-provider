from abc import ABC, abstractmethod
from uuid import UUID

from mypy.build import TypedDict

from application.user.reset_pwd.service import ResetPasswordToken


class NotifyService(ABC):
    @abstractmethod
    async def pwd_reset_notify(
        self, user_email: str, reset_pwd_token: ResetPasswordToken
    ) -> None:
        pass
