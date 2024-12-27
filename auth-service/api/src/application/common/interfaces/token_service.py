from uuid import uuid4

from application.common.token_types import Payload
from domain.entities.user.model import User


class TokenService:
    def __init__(self, jwt_service, redis_client, jwt_settings):
        self.jwt_service = jwt_service
        self.redis_client = redis_client
        self.jwt_settings = jwt_settings

    def create_access_token(self, user: User) -> str:
        payload: Payload = {
            "sub": str(user.id.value),
            "email": user.email.value,
            "role_id": user.role_id.value,
            "scope": user.get_scopes(),
        }
        token = self.jwt_service.encode(
            payload,
            expire_minutes=self.jwt_settings.access_token_expire_minutes,
        )
        return token

    def create_refresh_token(self, user: User) -> str:
        payload = {
            "sub": str(user.id.value),
            "jti": str(uuid4()),
        }
        token = self.jwt_service.encode(
            payload,
            expire_days=self.jwt_settings.refresh_token_expire_days,
        )
        return token

    async def whitelist_token(self, token: str):
        await self.redis_client.set(
            f"whitelist:{token}",
            "valid",
            ex=self.jwt_settings.access_token_expire_minutes * 60,
        )
