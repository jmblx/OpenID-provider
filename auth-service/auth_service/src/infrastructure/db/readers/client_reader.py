import logging

from sqlalchemy import select, text, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from application.common.interfaces.role_repo import RoleRepository
from application.common.views.client_view import ClientView, ClientsIdsData
from domain.entities.client.model import Client
from domain.entities.client.value_objects import ClientID
from domain.exceptions.client import ClientNotFound
from infrastructure.db.models import client_table
from application.client.common.client_reader import (
    ClientReader,
    ClientAuthData,
)
from infrastructure.db.readers.common import change_layout

logger = logging.getLogger(__name__)


class ClientReaderImpl(ClientReader):
    def __init__(self, db_session: AsyncSession, role_repo: RoleRepository):
        self.session = db_session
        self.role_repo = role_repo

    async def read_for_auth_page(
        self, client_id: ClientID
    ) -> ClientAuthData | None:
        query = select(client_table).where(client_table.c.id == client_id)
        result = await self.session.execute(query)
        client = result.mappings().first()
        return (
            ClientAuthData(client["name"], client["allowed_redirect_urls"])
            if client
            else None
        )

    async def read_for_client_page(
        self, client_id: ClientID
    ) -> ClientView | None:
        client = await self.session.get(Client, client_id)
        if not client:
            raise ClientNotFound()
        client_data: ClientView = {
            "name": client.name.value,
            "base_url": client.base_url.value,
            "allowed_redirect_urls": client.allowed_redirect_urls.value,
            "type": client.type.value,
        }
        # client_roles = await self.role_repo.get_roles_by_client_id(client_id, order_by_id=True)
        # if client_roles:
        #     client_data["roles"] = [
        #         typing.cast(
        #             RoleViewWithId,
        #             {
        #                 "id": role.id,
        #                 "name": role.name.value,
        #                 "base_scopes": role.base_scopes.to_list(),
        #                 "is_base": role.is_base,
        #             },
        #         )
        #         for role in client_roles
        #     ]
        return client_data

    async def read_all_clients_ids_data(
        self, from_: int, limit: int
    ) -> dict[ClientID, ClientsIdsData]:
        query = select(Client.id, Client.name).where(Client.id > from_).limit(limit)
        data = await self.session.execute(query)
        clients_data = data.mappings().all()
        result = {
            client["id"]: ClientsIdsData(name=client["name"].value)
            for client in clients_data
        }
        return result

    async def find_by_marks(
        self, input: str, similarity: float = 0.3
    ) -> dict[ClientID, ClientsIdsData] | None:
        await self.session.execute(
            text(f"SET LOCAL pg_trgm.similarity_threshold = {similarity};")
        )
        marks_converted = change_layout(input)
        query = select(Client.id, Client.name).where(
            or_(
                client_table.search_name.op("%")(input),
                client_table.search_name.op("%")(marks_converted),
            )
        )
        clients_data = (await self.session.execute(query)).mappings().all()
        result = {
            client["id"]: ClientsIdsData(name=client["name"].value)
            for client in clients_data
        }
        return result

    # async def search_clients(self, search_term: str) -> list[ClientView]:

