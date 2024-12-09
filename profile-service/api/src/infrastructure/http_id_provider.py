from application.auth.interfaces.jwt_service import JWTService
from application.auth.token_types import AccessToken
from application.common.id_provider import HttpIdentityProvider


class HttpIdentityProviderImpl(HttpIdentityProvider):
    """Провайдер для получения данных пользователя на основе AccessToken."""

    def __init__(self, jwt_service: JWTService, user_repo: UserRepository):
        self.jwt_service = jwt_service
        self.user_repo = user_repo

    async def get_user_by_access_token(self, token: AccessToken) -> User:
        payload = self.jwt_service.decode(token)
        user_id = payload.get("sub")
        return await self.user_repo.get_by_id(user_id)
