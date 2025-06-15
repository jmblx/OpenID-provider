from uuid import UUID

from pydantic import BaseModel, HttpUrl


class PaginationData(BaseModel):
    after_id: int = 0
    page_size: int = 10


class UserSchema(BaseModel):
    id: UUID
    email: str
    is_admin: bool
    avatar_update_timestamp: int
