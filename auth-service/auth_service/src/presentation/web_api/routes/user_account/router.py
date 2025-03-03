import logging
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import ORJSONResponse

from application.auth_as.identify_by_cookies_query import (
    IdentifyByCookiesQueryHandler,
)
from application.dtos.set_image import ImageDTO
from application.user.add_role_to_user_handler import (
    AddRoleToUserHandler,
    AddRoleToUserCommand,
)
from application.user.delete_user_handler import (
    DeleteUserHandler,
    DeleteUserCommand,
)
from application.user.set_user_avatar_handler import SetUserAvatarHandler, SetUserAvatarCommand

user_account_router = APIRouter(route_class=DishkaRoute, tags=["user_account"])


logger = logging.getLogger(__name__)


@user_account_router.delete("/user/{user_id}")
async def delete_user_account(
    user_id: UUID,
    handler: FromDishka[DeleteUserHandler],
):
    command = DeleteUserCommand(user_id)
    await handler.handle(command)


@user_account_router.get("/add-role/{user_id}/{role_id}")
async def add_role_to_user(
    handler: FromDishka[AddRoleToUserHandler], user_id: UUID, role_id: int
):
    command = AddRoleToUserCommand(user_id, role_id)
    await handler.handle(command)


@user_account_router.get("/me")
async def get_me(handler: FromDishka[IdentifyByCookiesQueryHandler]):
    return await handler.handle()

@user_account_router.post("/set-avatar")
async def set_avatar(handler: FromDishka[SetUserAvatarHandler], file: UploadFile = File(...)) -> ORJSONResponse:
    if not file:
        raise HTTPException(status_code=400, detail="Файл не был передан")

    content = await file.read()

    image_dto = ImageDTO(
        filename=file.filename,
        content=content,
        content_type=file.content_type
    )
    avatar_path = await handler.handle(SetUserAvatarCommand(image_dto))

    return ORJSONResponse({"avatar_path": avatar_path})
