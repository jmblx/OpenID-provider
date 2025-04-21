from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from application.user.reset_pwd.reset_pwd_with_token import (
    ResetPasswordWithTokenHandler, ResetPasswordWithTokenCommand,
)
from application.user.reset_pwd.request_change_pwd_handler import (
    RequestChangePasswordCommand,
    RequestChangePasswordHandler,
)
from application.user.reset_pwd.verify_reset_code_handler import VerifyResetCodeCommand, VerifyResetCodeHandler
from presentation.web_api.routes.user_password.dto import ResetPasswordDTO

user_password_router = APIRouter(
    route_class=DishkaRoute, tags=["user_password"]
)


@user_password_router.post("/user/password/reset/request-code")
async def request_reset_password(
    command: RequestChangePasswordCommand,
    handler: FromDishka[RequestChangePasswordHandler],
):
    await handler.handle(command)
    return {"status": "code_sent"}

@user_password_router.post("/user/password/reset/verify-code")
async def verify_reset_code(
    command: VerifyResetCodeCommand,
    handler: FromDishka[VerifyResetCodeHandler],
):
    result = await handler.handle(command)
    return {"reset_token": result.reset_token}

@user_password_router.post("/user/password/reset/confirm")
async def reset_password_with_token(
    command: ResetPasswordWithTokenCommand,
    handler: FromDishka[ResetPasswordWithTokenHandler],
):
    await handler.handle(command)
    return {"status": "password_changed"}
