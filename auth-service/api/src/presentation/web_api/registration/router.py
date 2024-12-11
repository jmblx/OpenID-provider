from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from starlette import status

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
from presentation.web_api.utils import render_auth_code_url

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
) -> ORJSONResponse:
    auth_code = await handler.handle(command)
    redirect_url = render_auth_code_url(command.redirect_url, auth_code)
    return ORJSONResponse(
        {"redirect_url": redirect_url}, status_code=status.HTTP_201_CREATED
    )
