import logging
from uuid import UUID

from fastapi import HTTPException

from application.common.exceptions import FingerprintMismatchException
from application.common.interfaces.http_auth import HttpAuthServerService
from application.common.interfaces.jwt_service import JWTService
from application.common.interfaces.white_list import TokenWhiteListService
from application.common.services.pkce import (
    PKCEService,
)
from application.common.auth_server_token_types import (
    Fingerprint,
    AccessToken,
    RefreshToken,
    AuthServerAccessTokenPayload,
)
from application.common.interfaces.auth_server_token_creation import AuthServerTokenCreationService
from application.common.interfaces.user_repo import UserRepository
from domain.entities.user.model import User
from domain.entities.user.value_objects import Email, RawPassword, UserID
from domain.common.services.pwd_service import PasswordHasher
from infrastructure.services.auth.config import JWTSettings
from application.common.services.auth_code import (
    AuthorizationCodeStorage,
)

logger = logging.getLogger(__name__)


class HttpAuthServerServerServiceImpl(HttpAuthServerService):
    """Сервис для аутентификации, обновления и управления токенами."""

    def __init__(
        self,
        user_repository: UserRepository,
        jwt_service: JWTService,
        token_creation_service: AuthServerTokenCreationService,
        token_whitelist_service: TokenWhiteListService,
        hash_service: PasswordHasher,
        jwt_settings: JWTSettings,
        auth_code_storage: AuthorizationCodeStorage,
        pkce_service: PKCEService,
    ):
        self.user_repository = user_repository
        self.jwt_service = jwt_service
        self.token_creation_service = token_creation_service
        self.token_whitelist_service = token_whitelist_service
        self.hash_service = hash_service
        self.jwt_settings = jwt_settings
        self.auth_code_storage = auth_code_storage
        self.pkce_service = pkce_service

    def _get_token_jti(self, refresh_token: RefreshToken) -> UUID:
        payload = self.jwt_service.decode(refresh_token)
        return payload["jti"]

    async def revoke(self, refresh_token: RefreshToken) -> None:
        jti = self._get_token_jti(refresh_token)
        await self.token_whitelist_service.remove_token(jti)

    async def invalidate_other_tokens(
        self, refresh_token: RefreshToken, fingerprint: Fingerprint
    ) -> None:
        payload: AuthServerAccessTokenPayload = self.jwt_service.decode(refresh_token)
        jti = payload["jti"]
        if not await self.token_whitelist_service.is_fingerprint_matching(
            jti, fingerprint
        ):
            raise FingerprintMismatchException()
        user_id: UUID = payload["sub"]  # type: ignore
        await self.token_whitelist_service.remove_tokens_except_current(
            jti, user_id
        )

    # async def authenticate_by_auth_code(
    #     self,
    #     auth_code: str,
    #     redirect_url: str,
    #     fingerprint: Fingerprint,
    #     code_challenger: str,
    #     user_scopes: list[str],
    # ) -> tuple[AccessToken, RefreshToken]:
    #     auth_code_data = await self.auth_code_storage.retrieve_auth_code_data(
    #         auth_code
    #     )
    #     if not auth_code_data:
    #         raise HTTPException(
    #             status_code=400, detail="Invalid authorization code"
    #         )
    #
    #     if auth_code_data["redirect_url"] != redirect_url:
    #         raise HTTPException(status_code=400, detail="Invalid redirect URL")
    #
    #     real_code_challenger = auth_code_data["code_challenger"]
    #     if not self._validate_pkce(code_challenger, real_code_challenger):
    #         raise HTTPException(status_code=400, detail="Invalid PKCE")
    #
    #     user = await self.user_repository.get_by_id(
    #         UserID(UUID(auth_code_data["user_id"]))
    #     )
    #     if not user:
    #         raise HTTPException(status_code=404, detail="User not found")
    #
    #     tokens = await self.create_and_save_tokens(user, fingerprint, client_id=int(auth_code_data["client_id"]), user_scopes=user_scopes)
    #     await self.auth_code_storage.delete_auth_code_data(auth_code)
    #     return tokens

    async def create_and_save_tokens(
        self,
        user: User,
        fingerprint: Fingerprint,
        user_scopes: list[str],
        client_id: int,
    ) -> tuple[AccessToken, RefreshToken]:
        """Создаёт и сохраняет токены."""
        access_token = self.token_creation_service.create_access_token(
            user, user_scopes, client_id
        )
        refresh_token_data = (
            await self.token_creation_service.create_auth_server_refresh_token(
                user, fingerprint
            )
        )
        await self.token_whitelist_service.replace_refresh_token(
            refresh_token_data,
            self.jwt_settings.refresh_token_by_user_limit,
        )
        return access_token, refresh_token_data.token
