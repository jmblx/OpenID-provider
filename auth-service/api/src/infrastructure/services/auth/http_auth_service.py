from fastapi import HTTPException

from application.auth.services.jwt_service import JWTService
from application.auth.services.token_creation import TokenCreationService

from application.auth.services.http_auth import HttpAuthService
from application.auth.services.white_list import TokenWhiteListService
from application.auth.token_types import Fingerprint, AccessToken, RefreshToken
from application.common.id_provider import HttpIdentityProvider
from domain.entities.user.value_objects import Email, RawPassword
from domain.services.security.pwd_service import HashService
from domain.services.user.user_service_interface import UserService
from infrastructure.services.auth.config import JWTSettings


class HttpAuthServiceImpl(HttpAuthService):
    """Сервис для аутентификации, обновления и управления токенами."""

    def __init__(
        self,
        user_service: UserService,
        jwt_service: JWTService,
        token_creation_service: TokenCreationService,
        token_whitelist_service: TokenWhiteListService,
        hash_service: HashService,
        jwt_settings: JWTSettings,
    ):
        self.user_service = user_service
        self.jwt_service = jwt_service
        self.token_creation_service = token_creation_service
        self.token_whitelist_service = token_whitelist_service
        self.hash_service = hash_service
        self.jwt_settings = jwt_settings

    async def authenticate_user(
        self, email: Email, password: RawPassword, fingerprint: Fingerprint
    ) -> tuple[AccessToken, RefreshToken]:
        user = await self.user_service.get_by_email(email)
        if not user or not self.hash_service.check_password(
            password.value, user.hashed_password.value
        ):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        access_token = self.token_creation_service.create_access_token(user)
        refresh_token_data = self.token_creation_service.create_refresh_token(
            user, fingerprint
        )
        await self.token_whitelist_service.save_refresh_token(
            refresh_token_data
        )
        await self.token_whitelist_service.remove_old_tokens(
            user.id, fingerprint, self.jwt_settings.refresh_token_by_user_limit
        )
        return access_token, refresh_token_data.token

    async def refresh_access_token(
        self, refresh_token: RefreshToken, fingerprint: Fingerprint
    ) -> AccessToken:
        payload = self.jwt_service.decode(refresh_token)
        jti = payload.get("jti")
        token_data = await self.token_whitelist_service.get_refresh_token_data(
            jti
        )
        if not token_data or token_data.fingerprint != fingerprint:
            raise HTTPException(
                status_code=401, detail="Invalid refresh token or fingerprint"
            )
        user = await self.user_service.get_by_id(token_data.user_id)
        return self.token_creation_service.create_access_token(user)

    async def logout(self, refresh_token: RefreshToken) -> None:
        payload = self.jwt_service.decode(refresh_token)
        jti = payload.get("jti")
        await self.token_whitelist_service.remove_token(jti)
