from logging import getLogger

from application.client.common.client_reader import ClientReader
from application.common.views.client_view import ClientsIdsData
from domain.entities.client.value_objects import ClientID


logger = getLogger(__name__)


class GetAllClientsIdsHandler:
    def __init__(self, client_reader: ClientReader):
        self.client_reader = client_reader

    async def handle(self) -> dict[ClientID, ClientsIdsData]:
        clients_ids_data = await self.client_reader.read_all_clients_ids_data()
        # logger.info("clients_ids_data: %s", clients_ids_data)
        return clients_ids_data
