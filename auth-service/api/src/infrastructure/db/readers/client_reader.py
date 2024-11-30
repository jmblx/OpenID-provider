from sqlalchemy import select, and_, exists
from sqlalchemy.ext.asyncio import AsyncSession

from application.client.interfaces.reader import ClientReader
from domain.entities.client.model import Client
from domain.entities.client.value_objects import ClientID, ClientRedirectUrl
from infrastructure.db.models import client_table


class ClientReaderImpl(ClientReader):
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def with_id(self, client_id: ClientID) -> Client | None:
        client = await self.session.get(Client, client_id)
        return client

    async def check_client_redirection_by_id(
        self, client_id: ClientID, redirect_url: ClientRedirectUrl
    ) -> bool:
        stmt = select(
            exists().where(
                and_(
                    client_table.c.id == client_id,
                    client_table.c.allowed_redirect_urls.any(redirect_url),
                )
            )
        )

        result = await self.session.execute(stmt)
        return result.scalar()
