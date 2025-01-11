from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from application.user.reset_pwd.change_pwd_handler import (
    SetNewPasswordHandler,
    SetNewPasswordCommand,
)
from application.user.reset_pwd.request_change_pwd_handler import (
    RequestChangePasswordCommand,
    RequestChangePasswordHandler,
)
from presentation.web_api.routes.user_password.dto import ResetPasswordDTO

user_password_router = APIRouter(
    route_class=DishkaRoute, tags=["user_password"]
)


@user_password_router.post("/request-reset-password/")
async def request_reset_password(
    command: RequestChangePasswordCommand,
    handler: FromDishka[RequestChangePasswordHandler],
):
    await handler.handle(command)


@user_password_router.post("/reset-password/{token}")
async def reset_password(
    token: str,
    data: ResetPasswordDTO,
    handler: FromDishka[SetNewPasswordHandler],
):
    command = SetNewPasswordCommand(token, data.new_password)
    await handler.handle(command)
