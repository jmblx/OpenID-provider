from dataclasses import dataclass
from logging import getLogger

from Demos.mmapfile_demo import page_size

from application.client.common.client_reader import ClientReader
from application.common.views.client_view import ClientsIdsData
from domain.entities.client.value_objects import ClientID


logger = getLogger(__name__)


@dataclass
class GetClientsIdsQuery:
    page: int
    page_size: int


class GetClientsIdsHandler:
    def __init__(self, client_reader: ClientReader):
        self.client_reader = client_reader

    async def handle(self, query: GetClientsIdsQuery) -> dict[ClientID, ClientsIdsData]:
        clients_ids_data = await self.client_reader.read_all_clients_ids_data(from_=query.page_size * (query.page - 1), limit=query.page_size)
        # logger.info("clients_ids_data: %s", clients_ids_data)
        return clients_ids_data
