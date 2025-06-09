from pydantic import BaseModel

from domain.entities.client.value_objects import ClientTypeEnum
from presentation.web_api.routes.auth.models import UserAuthRequest


class ClientAuthResponseModel(BaseModel):
    client_name: str


class RoleViewModel(BaseModel):
    name: str
    base_scopes: list[str]
    is_base: bool


class RoleViewWithIdModel(RoleViewModel):
    id: int


class ClientViewModel(BaseModel):
    name: str
    base_url: str
    allowed_redirect_urls: list[str]
    type: ClientTypeEnum
    roles: list[RoleViewWithIdModel] | None = None
    avatar_url: str | None


class UpdateClientModel(BaseModel):
    name: str | None
    base_url: str | None
    allowed_redirect_urls: list[str] | None
    type: ClientTypeEnum | None
