from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from jinja2 import PackageLoader
from starlette import status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from application.auth.commands.register_user_command import RegisterUserCommand
from application.auth.handlers.register_user_handler import (
    RegisterUserHandler,
)
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
            "model": ErrorResponse[InvalidRedirectURLError | InvalidClientError],
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse[UserAlreadyExistsError],
        },
    },
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
async def registration(
    handler: FromDishka[RegisterUserHandler],
    command: RegisterUserCommand,
) -> RedirectResponse:
    auth_code = await handler.handle(command)
    redirect_url = f"{command.redirect_url}?code={auth_code}&state=xyz"
    return RedirectResponse(url=redirect_url, status_code=307)
