from abc import ABC, abstractmethod
from typing import NewType

from domain.entities.user.model import User
from domain.entities.user.value_objects import UserID, Email

OAuth2Token = NewType('OAuthToken', str)


class OauthIdentityProvider(ABC):
    @abstractmethod
    async def get_yandex_user_email(self, oauth_token: OAuth2Token) -> Email: ...

    @abstractmethod
    async def get_current_user(self, oauth_token: OAuth2Token) -> User: ...
