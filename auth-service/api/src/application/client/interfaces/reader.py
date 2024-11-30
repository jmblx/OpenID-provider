from abc import ABC, abstractmethod

from domain.entities.client.model import Client
from domain.entities.client.value_objects import ClientID, ClientRedirectUrl


class ClientReader(ABC):
    @abstractmethod
    async def with_id(self, client_id: ClientID) -> Client | None:
        pass

    @abstractmethod
    async def check_client_redirection_by_id(
        self, client_id: ClientID, redirect_url: ClientRedirectUrl
    ) -> bool:
        pass

    @abstractmethod
    async def check_client_redirection_by_id(
        self, client_id: ClientID, redirect_url: ClientRedirectUrl
    ) -> bool:
        pass
