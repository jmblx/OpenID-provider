from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from starlette import status
from starlette.responses import RedirectResponse, Response, JSONResponse

from application.auth.commands.code_to_token_command import CodeToTokenCommand
from application.auth.commands.register_user_command import RegisterUserCommand
from application.auth.handlers.code_to_token_handler import CodeToTokenHandler
from application.auth.handlers.register_user_handler import (
    RegisterUserCommandHandler,
)
from application.auth.token_types import Fingerprint
from domain.exceptions.auth import (
    InvalidClientError,
    InvalidRedirectURLError,
)
from domain.exceptions.user import UserAlreadyExistsError
from presentation.web_api.responses import ErrorResponse

reg_router = APIRouter(route_class=DishkaRoute, tags=["reg"])


@reg_router.post(
    "/register",
    responses={
        status.HTTP_307_TEMPORARY_REDIRECT: {
            "description": "redirection to invoice download link",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[
                InvalidRedirectURLError | InvalidClientError
            ],
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse[UserAlreadyExistsError],
        },
    },
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
async def registration(
    handler: FromDishka[RegisterUserCommandHandler],
    command: RegisterUserCommand,
) -> RedirectResponse:
    auth_code = await handler.handle(command)
    redirect_url = f"{command.redirect_url}?code={auth_code}&state=xyz"
    return RedirectResponse(url=redirect_url, status_code=307)


@reg_router.post("/code-to-token")
async def code_to_token(
    handler: FromDishka[CodeToTokenHandler],
    fingerprint: FromDishka[Fingerprint],
    command: CodeToTokenCommand,
) -> RedirectResponse:
    refresh_token, access_token = await handler.handle(command, fingerprint)
    print(f"Access Token: {access_token}")
    print(f"Refresh Token: {refresh_token}")

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
