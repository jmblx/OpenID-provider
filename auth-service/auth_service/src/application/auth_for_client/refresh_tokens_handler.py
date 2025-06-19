from application.auth_as.common.scopes_service import ScopesService
from application.common.auth_server_token_types import (
    Fingerprint,
)
from application.common.client_token_types import ClientTokens
from application.common.id_provider import ClientIdentityProvider
from application.common.interfaces.http_auth import HttpClientService
from application.common.interfaces.role_repo import RoleRepository


class RefreshClientTokensHandler:
    def __init__(
        self,
        auth_service: HttpClientService,
        idp: ClientIdentityProvider,
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
    ) -> ClientTokens:
        user = await self.idp.get_current_user()
        client_id = self.idp.get_current_client_id()
        rs_ids = self.idp.get_current_rs_ids()
        user_roles = await self.role_repo.get_user_roles_by_rs_ids(
            user.id, rs_ids
        )
        new_scopes = self.scopes_service.calculate_full_user_scopes_for_client(
            user_roles
        )
        return await self.auth_service.create_and_save_tokens(
            user, new_scopes, client_id, rs_ids
        )
