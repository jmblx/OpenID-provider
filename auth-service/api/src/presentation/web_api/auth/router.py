from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from starlette.responses import RedirectResponse

from application.auth.commands.auth_user_command import AuthenticateUserCommand
from application.auth.handlers.auth_user_handler import (
    AuthenticateUserCommandHandler,
)
from application.auth.token_types import Fingerprint

auth_router = APIRouter(route_class=DishkaRoute, tags=["auth"])


@auth_router.post("/auth/login")
async def login(
    command: AuthenticateUserCommand,
    handler: FromDishka[AuthenticateUserCommandHandler],
) -> RedirectResponse:
    auth_code = await handler.handle(command)
    redirect_url = f"{command.redirect_url}?code={auth_code}&state=xyz"
    return RedirectResponse(url=redirect_url, status_code=307)
