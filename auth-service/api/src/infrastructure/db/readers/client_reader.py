
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.client.value_objects import ClientID
from infrastructure.db.models import client_table
from application.client.reader import ClientReader, ClientAuthData


class ClientReaderImpl(ClientReader):
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def read_for_auth_page(self, client_id: ClientID) -> ClientAuthData | None:
        query = select(client_table).where(client_table.c.id == client_id.value)
        result = await self.session.execute(query)
        client = result.mappings().first()
        return ClientAuthData(client["name"], client["allowed_redirect_url"]) if client else None
