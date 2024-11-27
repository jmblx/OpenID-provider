from abc import abstractmethod, ABC

from application.dtos.client import ClientCreateDTO
from domain.entities.client.model import Client


class ClientRepository(ABC):
    @abstractmethod
    async def save(self, client: Client) -> ClientCreateDTO:
        pass
