from dataclasses import dataclass

from application.auth_for_client.common.allow_client_access_service import (
    RequiredResources,
)
from application.client.client_queries import ValidateClientRequest
from application.common.id_provider import IdentityProvider
from application.common.services.auth_code import AuthorizationCodeStorage, AuthCodeData
from application.common.services.client_service import ClientService
from application.common.services.pkce import PKCEData, PKCEService, PKCECodeChallengeMethod
from domain.exceptions.user import UnauthenticatedUserError


@dataclass
class GetMeDataCommand:
    client_id: int
    required_resources: RequiredResources
    redirect_url: str
    code_verifier: str
    code_challenge_method: PKCECodeChallengeMethod


@dataclass
class MeData:
    client_name: str
    auth_code: str
    redirect_url: str


class GetMeDataHandler:
    def __init__(
        self,
        idp: IdentityProvider,
        client_service: ClientService,
        auth_code_storage: AuthorizationCodeStorage,
        pkce_service: PKCEService,
    ):
        self.idp = idp
        self.client_service = client_service
        self.auth_code_storage = auth_code_storage
        self.pkce_service = pkce_service

    async def handle(
        self, command: GetMeDataCommand
    ) -> MeData:
        user = await self.idp.get_current_user()
        if not user:
            raise UnauthenticatedUserError()
        client = await self.client_service.get_validated_client(
            ValidateClientRequest(
                client_id=command.client_id,
                redirect_url=command.redirect_url,
            )
        )
        # await self.rs_service.add_rs_by_ids_to_user(
        #     user, command.required_resources["rs_ids"]
        # )
        auth_code = self.auth_code_storage.generate_auth_code()
        pkce_data = PKCEData(
            code_verifier=command.code_verifier,
            code_challenge_method=command.code_challenge_method,
        )
        auth_code_data: AuthCodeData = {
            "user_id": str(user.id.value),
            "client_id": str(command.client_id),
            "code_challenger": self.pkce_service.generate_code_challenge(
                pkce_data
            ),
            **command.required_resources
        }

        await self.auth_code_storage.store_auth_code_data(
            auth_code, auth_code_data, expiration_time=6000
        )
        return MeData(redirect_url=command.redirect_url, client_name=client.name.value, auth_code=auth_code)

