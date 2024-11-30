from application.auth.commands.register_client_command import (
    RegisterClientCommand,
)
from application.client.interfaces.repo import ClientRepository
from application.common.uow import Uow
from application.dtos.client import ClientCreateDTO
from domain.entities.client.model import Client
from domain.entities.client.value_objects import (
    ClientName,
    ClientBaseUrl,
    ClientRedirectUrl,
    ClientType,
)


class RegisterClientHandler:
    def __init__(self, client_repo: ClientRepository, uow: Uow):
        self.client_repo = client_repo
        self.uow = uow

    async def handle(self, command: RegisterClientCommand) -> ClientCreateDTO:
        client = Client.create(
            name=command.name,
            base_url=command.base_url,
            allowed_redirect_urls=command.allowed_redirect_urls,
            type=command.type,
        )
        client_dto = await self.client_repo.save(client)
        await self.uow.commit()
        return client_dto
