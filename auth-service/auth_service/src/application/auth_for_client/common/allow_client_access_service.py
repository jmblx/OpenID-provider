from abc import ABC, abstractmethod
from typing import TypedDict, Literal
from uuid import UUID, uuid4

from domain.entities.resource_server.value_objects import ResourceServerIds


class RequiredResources(TypedDict, total=False):
    user_data_needed: list[Literal["email", "avatar_path"]]
    rs_ids: ResourceServerIds


class AllowToClientTokenData(RequiredResources):
    redirect_url: str


class AllowClientAccessService(ABC):

    @staticmethod
    def generate_allow_to_client_token():
        return uuid4()

    @abstractmethod
    async def save_allow_to_client_token_data(
        self,
        allow_to_client_token: UUID,
        required_resources: AllowToClientTokenData,
    ): ...
