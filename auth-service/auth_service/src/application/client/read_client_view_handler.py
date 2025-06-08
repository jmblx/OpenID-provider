from dataclasses import dataclass

from application.client.common.client_reader import ClientReader
from application.common.views.client_view import ClientData
from domain.entities.client.value_objects import ClientID


@dataclass
class ReadClientPageViewQuery:
    client_id: int


class ReadClientPageViewQueryHandler:
    def __init__(self, client_reader: ClientReader):
        self.client_reader = client_reader

    async def handle(self, query: ReadClientPageViewQuery) -> ClientData:
        client_view = await self.client_reader.read_for_client_page(
            ClientID(query.client_id)
        )
        return client_view
