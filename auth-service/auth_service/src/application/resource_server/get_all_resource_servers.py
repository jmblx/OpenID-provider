from logging import getLogger

from application.common.views.rs_view import ResourceServerIdsData
from application.resource_server.common.rs_reader import ResourceServerReader
from domain.entities.resource_server.value_objects import ResourceServerID

logger = getLogger(__name__)


class GetAllRSIdsHandler:
    def __init__(self, rs_reader: ResourceServerReader):
        self.rs_reader = rs_reader

    async def handle(self) -> dict[ResourceServerID, ResourceServerIdsData]:
        rs_ids_data = await self.rs_reader.read_all_resource_server_ids_data()
        # logger.info("clients_ids_data: %s", clients_ids_data)
        return rs_ids_data
