from abc import ABC, abstractmethod

from application.auth.token_types import AccessToken, BaseToken
from domain.entities.user.model import User
from domain.entities.user.value_objects import Email


class IdentityProvider(ABC):
    @abstractmethod
    async def get_user_by_access_token(self, token: BaseToken) -> User: ...


class HttpIdentityProvider(IdentityProvider):
    """Провайдер для получения данных пользователя на основе AccessToken."""

    @abstractmethod
    async def get_user_by_access_token(self, token: AccessToken) -> User:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: Email):
        pass
