from typing import TypedDict
from uuid import UUID

from application.common.id_provider import UserIdentityProvider


class UserData(TypedDict):
    id: UUID
    email: str
    avatar_path: str
    is_admin: bool

class IdentifyByCookiesQueryHandler:
    def __init__(self, idp: UserIdentityProvider):
        self.idp = idp

    async def handle(self) -> UserData:
        user = await self.idp.get_current_user()

        return {
            "email": user.email.value,
            "id": user.id.value,
            "avatar_path": user.avatar_path,
            "is_admin": user.is_admin,
        }
