from application.client.commands.validate_client_request import ValidateClientRequest
from application.client.interfaces.repo import ClientRepository
from domain.entities.client.model import Client
from domain.entities.client.value_objects import ClientRedirectUrl, ClientID
from domain.exceptions.client import ClientNotFound


class ClientService:
    def __init__(self, client_repo: ClientRepository):
        self.client_repo = client_repo

    async def get_validated_client(self, data: ValidateClientRequest) -> Client:
        client = await self.client_repo.get_by_id(ClientID(data.client_id))
        if not client:
            raise ClientNotFound(data.client_id)
        await Client.validate_redirect_url(
            client=client, redirect_url=ClientRedirectUrl(data.redirect_url)
        )
        return client
