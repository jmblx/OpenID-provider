from dataclasses import dataclass
from uuid import UUID

from application.common.interfaces.imedia_storage import StorageServiceInterface
from application.common.interfaces.user_repo import UserRepository
from application.dtos.set_image import ImageDTO
from domain.entities.user.value_objects import UserID


@dataclass
class SetUserAvatarCommand:
    user_id: UUID
    image: ImageDTO


class SetUserAvatarHandler:
    def __init__(self, user_repo: UserRepository, media_storage: StorageServiceInterface):
        self.user_repo = user_repo
        self.media_storage = media_storage

    async def __call__(
        self,
        command: SetUserAvatarCommand,
    ) -> str:
        avatar_path = await self.media_storage.set_avatar(
            bucket_name="users",
            filename=command.image.filename,
            content=command.image.content,
            content_type=command.image.content_type,
        )
        await self.user_repo.update_user_fields_by_id(
            user_id=UserID(command.user_id), upd_data={"avatar_path": avatar_path}
        )
        return avatar_path
