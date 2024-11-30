from uuid import UUID

from fastapi import HTTPException

from application.auth.services.pkce import (
    PKCEService,
    PKCEData,
    PKCECodeChallengeMethod,
)
from application.auth.token_types import Fingerprint, AccessToken, RefreshToken
from application.auth.interfaces.jwt_service import JWTService
from application.auth.interfaces.token_creation import TokenCreationService
from application.auth.interfaces.http_auth import HttpAuthService
from application.auth.interfaces.white_list import TokenWhiteListService
from application.user.interfaces.reader import UserReader
from domain.entities.user.model import User
from domain.entities.user.value_objects import Email, RawPassword, UserID
from domain.common.services.pwd_service import PasswordHasher
from infrastructure.services.auth.config import JWTSettings
from application.auth.services.auth_code import (
    AuthorizationCodeStorage,
    AuthCodeData,
)


class HttpAuthServiceImpl(HttpAuthService):
    """Сервис для аутентификации, обновления и управления токенами."""

    def __init__(
        self,
        user_reader: UserReader,
        jwt_service: JWTService,
        token_creation_service: TokenCreationService,
        token_whitelist_service: TokenWhiteListService,
        hash_service: PasswordHasher,
        jwt_settings: JWTSettings,
        auth_code_storage: AuthorizationCodeStorage,
        pkce_service: PKCEService,
    ):
        self.user_service = user_reader
        self.jwt_service = jwt_service
        self.token_creation_service = token_creation_service
        self.token_whitelist_service = token_whitelist_service
        self.hash_service = hash_service
        self.jwt_settings = jwt_settings
        self.auth_code_storage = auth_code_storage
        self.pkce_service = pkce_service

    async def authenticate_user(
        self, email: Email, password: RawPassword, fingerprint: Fingerprint
    ) -> tuple[AccessToken, RefreshToken]:
        user = await self.user_service.with_email(email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        self.hash_service.check_password(password, user.hashed_password)
        return await self._create_tokens(user, fingerprint)

    async def refresh_access_token(
        self, refresh_token: RefreshToken, fingerprint: Fingerprint
    ) -> AccessToken:
        payload = self.jwt_service.decode(refresh_token)
        jti = payload["jti"]
        token_data = await self.token_whitelist_service.get_refresh_token_data(
            jti
        )
        if not token_data or token_data.fingerprint != fingerprint:
            raise HTTPException(
                status_code=401, detail="Invalid refresh token or fingerprint"
            )
        user = await self.user_service.read_by_id(token_data.user_id)
        return self.token_creation_service.create_access_token(user)

    async def logout(self, refresh_token: RefreshToken) -> None:
        payload = self.jwt_service.decode(refresh_token)
        jti = payload["jti"]
        await self.token_whitelist_service.remove_token(jti)

    async def authenticate_by_auth_code(
        self,
        auth_code: str,
        redirect_url: str,
        fingerprint: Fingerprint,
        code_challenger: str,
    ) -> tuple[AccessToken, RefreshToken]:
        auth_code_data = await self.auth_code_storage.retrieve_auth_code_data(
            auth_code
        )
        if not auth_code_data:
            raise HTTPException(
                status_code=400, detail="Invalid authorization code"
            )

        if auth_code_data["redirect_url"] != redirect_url:
            raise HTTPException(status_code=400, detail="Invalid redirect URL")

        real_code_challenger = auth_code_data["code_challenger"]
        print(f"real_code_challenger: {real_code_challenger}\nuser_code: {code_challenger}")
        if not self._validate_pkce(code_challenger, real_code_challenger):
            raise HTTPException(status_code=400, detail="Invalid PKCE")

        user = await self.user_service.read_by_id(
            UserID(UUID(auth_code_data["user_id"]))
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        tokens = await self._create_tokens(user, fingerprint)
        await self.auth_code_storage.delete_auth_code_data(auth_code)
        return tokens

    async def _create_tokens(
        self, user: User, fingerprint: Fingerprint
    ) -> tuple[AccessToken, RefreshToken]:
        """Скрытая логика для создания токенов."""
        access_token = self.token_creation_service.create_access_token(user)
        refresh_token_data = (
            await self.token_creation_service.create_refresh_token(
                user, fingerprint
            )
        )
        await self.token_whitelist_service.save_refresh_token(
            refresh_token_data
        )
        await self.token_whitelist_service.remove_old_tokens(
            user.id,
            fingerprint,
            self.jwt_settings.refresh_token_by_user_limit,
        )
        return access_token, refresh_token_data.token

    def _validate_pkce(
        self, user_code_challenger: str, real_code_challenger: str
    ) -> bool:
        return user_code_challenger == real_code_challenger
