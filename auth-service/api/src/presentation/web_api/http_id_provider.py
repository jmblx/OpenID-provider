from application.auth.services.jwt_service import JWTService
from application.auth.token_types import AccessToken
from application.common.id_provider import HttpIdentityProvider
from domain.entities.user.model import User
from domain.services.user.user_service_interface import UserService


class HttpIdentityProviderImpl(HttpIdentityProvider):
    """Провайдер для получения данных пользователя на основе AccessToken."""

    def __init__(self, jwt_service: JWTService, user_service: UserService):
        self.jwt_service = jwt_service
        self.user_service = user_service

    async def get_user_by_access_token(self, token: AccessToken) -> User:
        payload = self.jwt_service.decode(token)
        user_id = payload.get("sub")
        return await self.user_service.get_by_id(user_id)
