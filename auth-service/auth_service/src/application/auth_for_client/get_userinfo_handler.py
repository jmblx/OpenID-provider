from collections import defaultdict
from typing import TypedDict
from uuid import UUID

from application.common.id_provider import ClientIdentityProvider
from application.common.interfaces.imedia_storage import StorageServiceInterface
from application.common.services.auth_code import ALLOWED_SCOPES
from domain.entities.user.model import User


class UserData(TypedDict, total=False):
    email: str
    id: UUID
    avatar_path: str


class GetUserInfoQueryHandler:
    def __init__(self, idp: ClientIdentityProvider, s3_storage: StorageServiceInterface):
        self.idp = idp
        self.s3_storage = s3_storage

    async def handle(self) -> UserData:
        user_scopes = self.idp.get_current_user_scopes()
        user: User = await self.idp.get_current_user()
        result = defaultdict(None)
        result["id"] = user.id.value
        available_data = [scope.split(":")[0] for scope in user_scopes if scope.split(":")[0] in ALLOWED_SCOPES]
        result = {
            k: getattr(getattr(user, k), "value", getattr(user, k))
            for k in available_data if k != "avatar_path"
        }
        try:
            if "avatar_path" in available_data:
                result["avatar_path"] = self.s3_storage.get_presigned_avatar_url(str(user.id.value))
        except ValueError: ...
        return result
        # result = {
        #     k: getattr(getattr(user, k), "value", getattr(user, k))
        #     for k in auth_code_data["user_data_needed"] if k != "avatar_path"
        # }
        # try:
        #     if idx := auth_code_data["user_data_needed"].index("avatar_path"):
        #         result["avatar_path"] = self.s3_storage.get_presigned_avatar_url(str(user.id.value))
        #         auth_code_data["user_data_needed"].pop(idx)
        # except ValueError: ...