from dataclasses import dataclass

from application.common.id_provider import UserIdentityProvider
from application.common.interfaces.user_repo import UserRepository
from application.dtos.set_image import ImageDTO
from application.common.interfaces.imedia_storage import UserS3StorageService


@dataclass
class SetUserAvatarCommand:
    image: ImageDTO


class SetUserAvatarHandler:
    def __init__(
        self,
        user_repo: UserRepository,
        media_storage: UserS3StorageService,
        idp: UserIdentityProvider,
    ):
        self.user_repo = user_repo
        self.media_storage = media_storage
        self.idp = idp

    async def handle(
        self,
        command: SetUserAvatarCommand,
    ) -> str:
        user = await self.idp.get_current_user()
        avatar_path = await self.media_storage.set_avatar(
            content=command.image.content,
            content_type=command.image.content_type,
            object_id=str(user.id.value),
        )
        return avatar_path
