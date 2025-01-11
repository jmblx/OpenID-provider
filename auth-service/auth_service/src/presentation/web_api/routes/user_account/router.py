from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from application.user.delete_account.handler import DeleteUserHandler, DeleteUserCommand

user_account_router = APIRouter(
    route_class=DishkaRoute, tags=["user_account"]
)


@user_account_router.delete("/user/{user_id}")
async def request_reset_password(
    user_id: UUID,
    handler: FromDishka[DeleteUserHandler],
):
    command = DeleteUserCommand(user_id)
    await handler.handle(command)
