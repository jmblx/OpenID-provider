from uuid import UUID

from pydantic import BaseModel
from pydantic.v1 import HttpUrl


class PaginationData(BaseModel):
    after_id: int = 0
    page_size: int = 10


class UserSchema(BaseModel):
    id: UUID
    email: str
    avatar_path: HttpUrl
    is_admin: bool
