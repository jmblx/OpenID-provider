from abc import ABC, abstractmethod
from datetime import timedelta

from application.auth.token_types import JwtToken, Payload, BaseToken


class JWTService(ABC):
    """Абстракция для работы с JWT токенами."""

    @abstractmethod
    def encode(
        self,
        payload: Payload,
    ) -> JwtToken:
        """Создание JWT токена с заданным сроком действия."""

    @abstractmethod
    def decode(self, token: BaseToken) -> Payload:
        """Декодирование JWT токена."""
