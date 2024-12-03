from application.auth.commands.auth_user_command import AuthenticateUserCommand
from application.auth.services.auth_code import AuthorizationCodeStorage, AuthCodeData
from application.auth.services.pkce import PKCEData, PKCEService
from application.client.interfaces.reader import ClientReader
from application.common.uow import Uow
from application.user.interfaces.reader import UserReader
from application.user.interfaces.repo import UserRepository
from domain.entities.client.model import Client
from domain.entities.client.value_objects import ClientID, ClientRedirectUrl
from domain.entities.user.model import User
from domain.entities.user.value_objects import Email
from domain.common.services.pwd_service import PasswordHasher
from domain.exceptions.user import UserNotFoundByEmailError


class AuthenticateUserHandler:
    def __init__(
        self,
        user_reader: UserReader,
        auth_code_storage: AuthorizationCodeStorage,
        client_reader: ClientReader,
        user_repository: UserRepository,
        uow: Uow,
        pkce_service: PKCEService
    ):
        self.user_reader = user_reader
        self.user_repository = user_repository
        self.auth_code_storage = auth_code_storage
        self.client_reader = client_reader
        self.uow = uow
        self.pkce_service = pkce_service

    async def handle(self, command: AuthenticateUserCommand) -> str:
        client: Client = await self.client_reader.with_id(ClientID(command.client_id)) #type: ignore
        await Client.validate_redirect_url(
            client=client,
            redirect_url=ClientRedirectUrl(command.redirect_url)
        )
        user = await self.user_reader.by_fields_with_clients({"email": Email(command.email)})
        if not user:
            raise UserNotFoundByEmailError(command.email)
        if client not in user.clients:
            user.clients.append(client)
            await self.uow.commit()
        auth_code = self.auth_code_storage.generate_auth_code()
        pkce_data = PKCEData(code_verifier=command.code_verifier, code_challenge_method=command.code_challenge_method)

        auth_code_data: AuthCodeData = {
            "user_id": str(user.id.value),
            "client_id": str(command.client_id),
            "redirect_url": command.redirect_url,
            "code_challenger": self.pkce_service.generate_code_challenge(pkce_data),
        }

        await self.auth_code_storage.store_auth_code_data(
            auth_code,
            auth_code_data,
            expiration_time=6000
        )

        return auth_code
