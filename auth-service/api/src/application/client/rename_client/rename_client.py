from dataclasses import dataclass

from application.common.interfaces.client_repo import ClientRepository
from application.common.uow import Uow
from domain.entities.client.model import Client
from domain.entities.client.value_objects import ClientID
from domain.exceptions.client import ClientNotFound


@dataclass(frozen=True)
class RenameClientCommand:
    new_name: str


class RenameClientCommandHandler:
    def __init__(self, client_repo: ClientRepository, uow: Uow):
        self.client_repo = client_repo
        self.uow = uow

    async def handle(self, command: RenameClientCommand, client_id: int) -> None:
        client: Client | None = await self.client_repo.get_by_id(ClientID(client_id))
        if not client:
            raise ClientNotFound()
        client.rename(command.new_name)
        await self.uow.commit()
