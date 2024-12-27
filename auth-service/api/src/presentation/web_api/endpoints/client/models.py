from pydantic import BaseModel

from presentation.web_api.endpoints.auth.models import UserAuthRequest


class UserRegisterRequest(UserAuthRequest):
    role_id: int


class ClientAuthResponseModel(BaseModel):
    client_name: str
