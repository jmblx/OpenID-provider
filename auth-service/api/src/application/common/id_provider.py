from abc import ABC, abstractmethod

from application.auth.interfaces import jwt_service
from application.auth.interfaces.jwt_service import JWTService
from application.auth.token_types import AccessToken, BaseToken
from domain.entities.user.model import User
from domain.entities.user.value_objects import Email, UserID


class IdentityProvider(ABC):
    @abstractmethod
    async def get_current_user_id(self) -> UserID: ...


class HttpIdentityProvider(IdentityProvider):
    def __init__(self, jwt_service: JWTService, access_token: AccessToken):
        self.access_token = access_token
        self.jwt_service = jwt_service

    async def get_current_user_id(self) -> UserID:
        payload = self.jwt_service.decode(self.access_token)
        return UserID(payload['sub'])
