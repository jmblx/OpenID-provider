from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from application.user.add_role_to_user_handler import (
    AddRoleToUserHandler,
    AddRoleToUserCommand,
)
from application.user.delete_user_handler import (
    DeleteUserHandler,
    DeleteUserCommand,
)

user_account_router = APIRouter(route_class=DishkaRoute, tags=["user_account"])


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
