from application.auth.scopes_service import ScopesService
from application.common.id_provider import IdentityProvider
from application.common.interfaces.http_auth import HttpAuthService
from application.common.interfaces.role_repo import RoleRepository
from application.common.token_types import (
    AccessToken,
    RefreshToken,
    Fingerprint,
)


class RefreshTokensHandler:
    def __init__(
        self,
        auth_service: HttpAuthService,
        idp: IdentityProvider,
        fingerprint: Fingerprint,
        scopes_service: ScopesService,
        role_repo: RoleRepository,
    ):
        self.auth_service = auth_service
        self.idp = idp
        self.fingerprint = fingerprint
        self.scopes_service = scopes_service
        self.role_repo = role_repo

    async def handle(
        self,
    ) -> tuple[AccessToken, RefreshToken]:
        user = await self.idp.get_current_user()
        client_id = self.idp.get_current_client_id()
        user_roles = await self.role_repo.get_user_roles_by_client_id(
            user.id, client_id
        )
        new_scopes = self.scopes_service.calculate_full_user_scopes_for_client(
            user_roles
        )
        return await self.auth_service.create_and_save_tokens(
            user, self.fingerprint, new_scopes, client_id
        )
