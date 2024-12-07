from application.auth.commands.auth_user_command import AuthenticateUserCommand
from application.auth.services.auth_code import AuthorizationCodeStorage, AuthCodeData
from application.auth.services.pkce import PKCEData, PKCEService
from application.client.commands.validate_client_request import ValidateClientRequest
from application.client.service import ClientService
from application.common.uow import Uow
from application.user.interfaces.repo import UserRepository
from domain.entities.user.value_objects import Email
from domain.exceptions.user import UserNotFoundByEmailError


class AuthenticateUserHandler:
    def __init__(
        self,
        auth_code_storage: AuthorizationCodeStorage,
        client_service: ClientService,
        user_repository: UserRepository,
        uow: Uow,
        pkce_service: PKCEService,
    ):
        self.user_repository = user_repository
        self.auth_code_storage = auth_code_storage
        self.client_service = client_service
        self.uow = uow
        self.pkce_service = pkce_service

    async def handle(self, command: AuthenticateUserCommand) -> str:
        client = await self.client_service.get_validated_client(
            ValidateClientRequest(
                client_id=command.client_id,
                redirect_url=command.redirect_url,
            )
        )
        user = await self.user_repository.by_fields_with_clients(
            {"email": Email(command.email)}
        )
        if not user:
            raise UserNotFoundByEmailError(command.email)
        if client not in user.clients:
            user.clients.append(client)
            await self.uow.commit()
        auth_code = self.auth_code_storage.generate_auth_code()
        pkce_data = PKCEData(
            code_verifier=command.code_verifier,
            code_challenge_method=command.code_challenge_method,
        )

        auth_code_data: AuthCodeData = {
            "user_id": str(user.id.value),
            "client_id": str(command.client_id),
            "redirect_url": command.redirect_url,
            "code_challenger": self.pkce_service.generate_code_challenge(pkce_data),
        }

        await self.auth_code_storage.store_auth_code_data(
            auth_code, auth_code_data, expiration_time=6000
        )

        return auth_code
