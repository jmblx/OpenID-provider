from dataclasses import dataclass
from uuid import UUID

from application.common.id_provider import UserIdentityProvider
from application.common.interfaces.imedia_storage import (
    StorageServiceInterface,
)
from application.common.interfaces.user_repo import UserRepository
from application.common.uow import Uow
from application.dtos.set_image import ImageDTO
from domain.entities.user.value_objects import UserID


@dataclass
class SetUserAvatarCommand:
    image: ImageDTO


class SetUserAvatarHandler:
    def __init__(
        self,
        user_repo: UserRepository,
        media_storage: StorageServiceInterface,
        uow: Uow,
        idp: UserIdentityProvider,
    ):
        self.user_repo = user_repo
        self.media_storage = media_storage
        self.uow = uow
        self.idp = idp

    async def handle(
        self,
        command: SetUserAvatarCommand,
    ) -> str:
        user = await self.idp.get_current_user()
        avatar_path = self.media_storage.set_avatar(
            filename=command.image.filename,
            content=command.image.content,
            content_type=command.image.content_type,
            user_id=str(user.id.value),
        )
        user.avatar_path = avatar_path
        await self.uow.commit()
        return avatar_path
