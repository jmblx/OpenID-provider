from application.auth.commands.register_client_command import (
    RegisterClientCommand,
)
from application.client.interfaces.repo import ClientRepository
from application.common.uow import Uow
from application.dtos.client import ClientCreateDTO
from domain.entities.client.model import Client
from domain.entities.client.value_objects import ClientName, ClientBaseUrl, ClientRedirectUrl, ClientType


class RegisterClientHandler:
    def __init__(
        self,
        client_repo: ClientRepository,
        uow: Uow
    ):
        self.client_repo = client_repo
        self.uow = uow

    async def handle(self, command: RegisterClientCommand) -> ClientCreateDTO:
        name = ClientName(command.name)
        base_url = ClientBaseUrl(command.base_url)
        allowed_redirect_urls = [
            ClientRedirectUrl(client) for client in command.allowed_redirect_urls
        ]
        client_type = ClientType(command.type)
        client = Client.create(
            name=name,
            base_url=base_url,
            allowed_redirect_urls=allowed_redirect_urls,
            type=client_type,
        )
        await self.client_repo.save(client)
        await uow.commit()
