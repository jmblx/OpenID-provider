from typing import TypedDict
from uuid import UUID

from application.common.id_provider import UserIdentityProvider
from application.common.interfaces.imedia_storage import StorageService


class UserData(TypedDict):
    id: UUID
    email: str
    avatar_path: str
    is_admin: bool

class IdentifyByCookiesQueryHandler:
    def __init__(self, idp: UserIdentityProvider, s3_storage: StorageService):
        self.idp = idp
        self.s3_storage = s3_storage

    async def handle(self) -> UserData:
        user = await self.idp.get_current_user()

        return {
            "email": user.email.value,
            "id": user.id.value,
            "avatar_path": self.s3_storage.get_presigned_avatar_url(str(user.id.value)),
            "is_admin": user.is_admin,
        }
