from typing import Literal
from uuid import UUID

from pydantic import BaseModel, HttpUrl

from application.client.client_queries import ValidateClientRequest
from application.common.services.pkce import PKCECodeChallengeMethod, PKCEData


class UserAuthRequest(ValidateClientRequest, PKCEData): ...


class RequiredResources(BaseModel):
    user_data_needed: list[Literal["email", "avatar_path"]] | None = None
    rs_ids: list[int] | None = None


class GetMePageDataSchema(BaseModel):
    client_id: int
    required_resources: RequiredResources
    redirect_url: HttpUrl
    code_verifier: str
    code_challenge_method: PKCECodeChallengeMethod


class CodeToTokenResponseSchema(BaseModel):
    email: str | None
    avatar_path: str | None


class NewActiveUserSchema(BaseModel):
    new_active_user_id: UUID | None
