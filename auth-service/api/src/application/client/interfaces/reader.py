from abc import ABC, abstractmethod

from domain.entities.client.model import Client
from domain.entities.client.value_objects import ClientID


class ClientReader(ABC):
    @abstractmethod
    async def with_id(self, client_id: ClientID) -> Client:
        pass
