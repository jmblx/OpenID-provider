import json
from datetime import timedelta

from application.common.interfaces.jwt_service import JWTService
from application.common.interfaces.auth_server_token_creation import AuthServerTokenCreationService
from application.common.auth_server_token_types import AccessToken, RefreshTokenWithData
from uuid import uuid4, UUID

from infrastructure.services.auth.config import JWTSettings


class AuthServerTokenCreationServiceImpl(AuthServerTokenCreationService):
    """Реализация сервиса создания токенов с использованием JWTService."""

    def __init__(self, jwt_settings: JWTSettings, jwt_service: JWTService):
        self.jwt_service = jwt_service
        self.jwt_settings = jwt_settings

    def create_auth_server_access_token(
        self, user_id: UUID, is_admin
    ) -> AccessToken:
        jwt_payload = {
            "sub": str(user_id),
            "jti": str(uuid4()),
            "is_admin": is_admin,
        }
        encoded_token = self.jwt_service.encode(
            payload=jwt_payload,
            expire_minutes=self.jwt_settings.access_token_expire_minutes,
        )
        return AccessToken(encoded_token["token"])

    async def create_auth_server_refresh_token(
        self, user_id: UUID, fingerprint: str
    ) -> RefreshTokenWithData:
        jti = str(uuid4())
        jwt_payload = {"sub": str(user_id), "jti": jti}
        encoded_token = self.jwt_service.encode(
            payload=jwt_payload,
            expire_timedelta=timedelta(
                days=self.jwt_settings.refresh_token_expire_days
            ),
        )
        refresh_token_data = RefreshTokenWithData(
            token=encoded_token["token"],
            user_id=user_id,
            jti=jti,
            fingerprint=fingerprint,
            created_at=encoded_token["created_at"],
        )
        return refresh_token_data
