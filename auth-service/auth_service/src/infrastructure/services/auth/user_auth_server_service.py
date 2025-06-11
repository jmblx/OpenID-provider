import logging
from uuid import UUID

from application.common.interfaces.http_auth import HttpAuthServerService
from application.common.interfaces.jwt_service import JWTService
from application.common.auth_server_token_types import (
    Fingerprint,
    AuthServerRefreshToken,
    AuthServerAccessTokenPayload, AuthServerTokens,
)
from application.common.interfaces.auth_server_token_creation import AuthServerTokenCreationService
from application.common.interfaces.white_list import AuthServerTokenWhitelistService
from domain.entities.user.model import User
from infrastructure.services.auth.config import JWTSettings

logger = logging.getLogger(__name__)


class HttpAuthServerServiceImpl(HttpAuthServerService):
    """Сервис для аутентификации, обновления и управления токенами."""

    def __init__(
        self,
        jwt_service: JWTService,
        token_creation_service: AuthServerTokenCreationService,
        token_whitelist_service: AuthServerTokenWhitelistService,
        jwt_settings: JWTSettings,
        fingerprint: Fingerprint,
    ):
        self.jwt_service = jwt_service
        self.token_creation_service = token_creation_service
        self.token_whitelist_service = token_whitelist_service
        self.jwt_settings = jwt_settings
        self.fingerprint = fingerprint

    def _get_token_jti(self, refresh_token: AuthServerRefreshToken) -> UUID:
        payload = self.jwt_service.decode(refresh_token)
        return payload["jti"]

    async def revoke(self, refresh_token: AuthServerRefreshToken) -> None:
        jti = self._get_token_jti(refresh_token)
        await self.token_whitelist_service.remove_token(jti)

    async def invalidate_other_tokens(
        self, refresh_token: AuthServerRefreshToken
    ) -> None:
        payload: AuthServerAccessTokenPayload = self.jwt_service.decode(refresh_token)
        jti = payload["jti"]
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
    # ) -> tuple[AuthServerAccessToken, AuthServerRefreshToken]:
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
        fingerprint: Fingerprint | None = None,
        is_admin: bool = False,
    ) -> AuthServerTokens:
        """Создаёт и сохраняет токены."""
        if not fingerprint:
            fingerprint = self.fingerprint
        user_id: UUID = user.id.value
        access_token = (
            self.token_creation_service.create_auth_server_access_token(
                user_id, is_admin
            )
        )
        refresh_token_data = (
            await self.token_creation_service.create_auth_server_refresh_token(
                user_id, fingerprint
            )
        )
        await (self.token_whitelist_service.
        replace_refresh_token(
            refresh_token_data,
            self.jwt_settings.refresh_token_by_user_limit,
        ))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token_data.token,
        }
