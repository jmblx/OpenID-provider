import logging

from application.client.commands.validate_client_request import ValidateClientRequest
from application.client.interfaces.repo import ClientRepository
from domain.entities.client.model import Client
from domain.entities.client.value_objects import ClientRedirectUrl, ClientID
from domain.exceptions.client import ClientNotFound


logger = logging.getLogger(__name__)


class ClientService:
    def __init__(self, client_repo: ClientRepository):
        self.client_repo = client_repo

    async def get_validated_client(self, data: ValidateClientRequest) -> Client:
        client = await self.client_repo.get_by_id(ClientID(data.client_id))
        if not client:
            raise ClientNotFound()
        await Client.validate_redirect_url(
            allowed_redirect_urls=client.allowed_redirect_urls, redirect_url=ClientRedirectUrl(data.redirect_url)
        )
        logger.info(self.allowed_redirect_urls.value)
        return client
