from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.common.interfaces.rs_reader import ResourceServerData, ResourceServerReader
from domain.entities.resource_server.model import ResourceServer
from domain.entities.resource_server.value_objects import ResourceServerID
from infrastructure.db.models import rs_table


class ResourceServerReaderImpl(ResourceServerReader):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_resource_server_data_by_ids(self, rs_ids: list[ResourceServerID]) -> dict[
        ResourceServerID, ResourceServerData]:
        query = select(ResourceServer.id, ResourceServer.name).where(rs_table.c.id.in_(rs_ids))
        resource_servers = await self.session.execute(query)
        return {rs.id: {'name': rs.name} for rs in resource_servers}
