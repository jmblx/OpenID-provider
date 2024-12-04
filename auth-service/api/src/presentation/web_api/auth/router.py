from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from starlette.responses import RedirectResponse
from starlette.status import HTTP_307_TEMPORARY_REDIRECT

from application.auth.commands.auth_user_command import AuthenticateUserCommand
from application.auth.commands.code_to_token_command import CodeToTokenCommand
from application.auth.handlers.auth_user_handler import (
    AuthenticateUserHandler,
)
from application.auth.handlers.code_to_token_handler import CodeToTokenHandler
from application.auth.token_types import Fingerprint

auth_router = APIRouter(route_class=DishkaRoute, tags=["auth"])


@auth_router.post("/login")
async def login(
    command: AuthenticateUserCommand,
    handler: FromDishka[AuthenticateUserHandler],
) -> RedirectResponse:
    auth_code = await handler.handle(command)
    redirect_url = f"{command.redirect_url}?code={auth_code}&state=xyz"
    return RedirectResponse(url=redirect_url, status_code=HTTP_307_TEMPORARY_REDIRECT)

@auth_router.post("/code-to-token")
async def code_to_token(
    handler: FromDishka[CodeToTokenHandler],
    fingerprint: FromDishka[Fingerprint],
    command: CodeToTokenCommand,
) -> RedirectResponse:
    access_token, refresh_token = await handler.handle(command, fingerprint)

    response = RedirectResponse(f"{command.redirect_url}?state=xyz")
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        max_age=60 * 60,
        expires=60 * 60,
        samesite="lax",
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        max_age=60 * 60 * 24 * 30,
        expires=60 * 60 * 24 * 30,
        samesite="lax",
    )
    return response
