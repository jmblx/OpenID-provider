import logging
from abc import ABC, abstractmethod
from typing import Annotated
from uuid import UUID

from dishka import FromComponent
from fastapi import HTTPException
from starlette import status

from application.common.client_token_types import ClientAccessToken, ClientRefreshToken
from application.common.interfaces.jwt_service import JWTService
from application.common.interfaces.user_repo import UserRepository
from application.common.interfaces.white_list import TokenWhiteListService
from application.common.auth_server_token_types import (
    AccessToken,
    RefreshToken,
    Fingerprint,
)
from domain.entities.client.value_objects import ClientID
from domain.entities.resource_server.value_objects import ResourceServerID
from domain.entities.user.model import User
from domain.entities.user.value_objects import UserID


class UserIdentityProvider(ABC):
    @abstractmethod
    async def get_current_user_id(self) -> UserID: ...

    @abstractmethod
    async def get_current_user(self) -> User: ...


class ClientIdentityProvider(UserIdentityProvider):
    @abstractmethod
    def get_current_client_id(self) -> ClientID: ...

    @abstractmethod
    def get_current_rs_ids(self) -> list[ResourceServerID]: ...


logger = logging.getLogger(__name__)


class BaseTokenProvider(ABC):
    def __init__(self, jwt_service: JWTService):
        self.jwt_service = jwt_service
        self._decoded_tokens = {}

    def _decode_token(self, token_name: str, token_value: str) -> dict:
        if token_name not in self._decoded_tokens:
            self._decoded_tokens[token_name] = self.jwt_service.decode(token_value)
        return self._decoded_tokens[token_name]


class UserIdentityProviderImpl(UserIdentityProvider, BaseTokenProvider):
    def __init__(
        self,
        access_token: AccessToken,
        refresh_token: RefreshToken,
        jwt_service: JWTService,
        user_repo: UserRepository,
        token_whitelist_service: Annotated[TokenWhiteListService, FromComponent("auth_server")],
        fingerprint: Fingerprint,
    ):
        super().__init__(jwt_service)
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.user_repo = user_repo
        self.token_whitelist_service = token_whitelist_service
        self.fingerprint = fingerprint

        self._access_token_payload = self._decode_token("access_token", self.access_token)
        self._refresh_token_payload = self._decode_token("refresh_token", self.refresh_token)

    def _get_refresh_token_jti(self) -> UUID:
        return self._refresh_token_payload["jti"]

    async def get_current_user_id(self) -> UserID:
        jti = self._get_refresh_token_jti()
        token_data = await self.token_whitelist_service.get_refresh_token_data(jti)
        logger.info("token data: %s", token_data)
        if not token_data or token_data.fingerprint != self.fingerprint:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token or fingerprint",
            )
        return UserID(token_data.user_id)

    async def get_current_user(self) -> User:
        user_id = await self.get_current_user_id()
        return await self.user_repo.get_by_id(user_id)


class ClientIdentityProviderImpl(ClientIdentityProvider, BaseTokenProvider):
    def __init__(
        self,
        client_access_token: ClientAccessToken,
        client_refresh_token: ClientRefreshToken,
        jwt_service: JWTService,
        user_repo: UserRepository,
        token_whitelist_service: Annotated[TokenWhiteListService, FromComponent("client")],
        fingerprint: Fingerprint,
    ):
        super().__init__(jwt_service)
        self.client_access_token = client_access_token
        self.client_refresh_token = client_refresh_token
        self.user_repo = user_repo
        self.token_whitelist_service = token_whitelist_service
        self.fingerprint = fingerprint

        self._client_access_token_payload = self._decode_token("client_access_token", self.client_access_token)
        self._client_refresh_token_payload = self._decode_token("client_refresh_token", self.client_refresh_token)

    def get_current_client_id(self) -> ClientID:
        return self._client_refresh_token_payload["client_id"]

    def get_current_rs_ids(self) -> list[ResourceServerID]:
        return self._client_refresh_token_payload["rs_ids"]

    def _get_refresh_token_jti(self) -> UUID:
        return self._client_refresh_token_payload["jti"]

    async def get_current_user_id(self) -> UserID:
        jti = self._get_refresh_token_jti()
        token_data = await self.token_whitelist_service.get_refresh_token_data(jti)
        logger.info("token data: %s", token_data)
        if not token_data or token_data.fingerprint != self.fingerprint:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token or fingerprint",
            )
        return UserID(token_data.user_id)

    async def get_current_user(self) -> User:
        user_id = await self.get_current_user_id()
        return await self.user_repo.get_by_id(user_id)
