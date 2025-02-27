from dataclasses import dataclass
from uuid import UUID

from fastapi import HTTPException

from application.auth_as.common.scopes_service import ScopesService
from application.common.interfaces.role_repo import RoleRepository
from application.common.interfaces.user_repo import UserRepository
from application.common.services.auth_code import AuthorizationCodeStorage
from application.common.auth_server_token_types import (
    AccessToken,
    RefreshToken,
    Fingerprint,
)
from application.common.interfaces.http_auth import HttpAuthServerService
from domain.entities.client.value_objects import ClientID
from domain.entities.user.value_objects import UserID


@dataclass
class CodeToTokenCommand:
    auth_code: str
    code_challenger: str
    redirect_url: str
    scopes: list[str]


class CodeToTokenHandler:
    def __init__(
        self,
        auth_service: HttpAuthServerService,
        scopes_service: ScopesService,
        role_repo: RoleRepository,
        auth_code_storage: AuthorizationCodeStorage,
        user_repository: UserRepository,
    ) -> None:
        self.auth_service = auth_service
        self.scopes_service = scopes_service
        self.role_repo = role_repo
        self.auth_code_storage = auth_code_storage
        self.user_repository = user_repository

    def _validate_pkce(
        self, user_code_challenger: str, real_code_challenger: str
    ) -> bool:
        return user_code_challenger == real_code_challenger

    async def handle(
        self, command: CodeToTokenCommand, fingerprint: Fingerprint
    ) -> tuple[AccessToken, RefreshToken]:
        auth_code_data = await self.auth_code_storage.retrieve_auth_code_data(
            command.auth_code
        )
        if not auth_code_data:
            raise HTTPException(
                status_code=400, detail="Invalid authorization code"
            )

        if auth_code_data["redirect_url"] != command.redirect_url:
            raise HTTPException(status_code=400, detail="Invalid redirect URL")

        real_code_challenger = auth_code_data["code_challenger"]
        if not self._validate_pkce(
            command.code_challenger, real_code_challenger
        ):
            raise HTTPException(status_code=400, detail="Invalid PKCE")

        user = await self.user_repository.get_by_id(
            UserID(UUID(auth_code_data["user_id"]))
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        client_id = int(auth_code_data["client_id"])
        user_roles = await self.role_repo.get_user_roles_by_client_id(
            user_id=user.id, client_id=ClientID(client_id)
        )
        user_scopes = (
            self.scopes_service.calculate_full_user_scopes_for_client(
                user_roles
            )
        )
        tokens = await self.auth_service.create_and_save_tokens(
            user, fingerprint, client_id=client_id, user_scopes=user_scopes
        )
        await self.auth_code_storage.delete_auth_code_data(command.auth_code)

        return tokens[0], tokens[1]
