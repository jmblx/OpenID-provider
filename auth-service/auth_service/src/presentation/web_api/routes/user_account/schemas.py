from pydantic import BaseModel


class ClientGetUserDataInfo(BaseModel):
    email: str | None
    avatar_path: str | None