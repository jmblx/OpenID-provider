from pydantic import BaseModel

from domain.entities.client.value_objects import ClientTypeEnum
from presentation.web_api.routes.auth.models import UserAuthRequest


class UserRegisterRequest(UserAuthRequest):
    role_id: int


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


class UpdateClientModel(BaseModel):
    name: str | None
    base_url: str | None
    allowed_urls: list[str] | None
    client_type: ClientTypeEnum | None
