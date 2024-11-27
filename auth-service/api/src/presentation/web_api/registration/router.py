from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from starlette import status
from starlette.responses import RedirectResponse

from application.auth.commands.register_user_command import RegisterUserCommand
from application.auth.handlers.register_user_handler import (
    RegisterUserCommandHandler,
)
from domain.exceptions.auth import (
    UserAlreadyExistsError,
    InvalidClientError,
    InvalidRedirectURLError,
)
from presentation.web_api.responses import ErrorResponse

router = APIRouter(route_class=DishkaRoute, tags=["reg", "auth"])


@router.post(
    "/user",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[
                InvalidRedirectURLError | InvalidClientError
            ],
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse[UserAlreadyExistsError],
        },
    },
)
async def registration(
    handler: FromDishka[RegisterUserCommandHandler],
    command: RegisterUserCommand,
) -> RedirectResponse:
    auth_code = await handler.handle(command)
    redirect_url = f"{command.redirect_url}?code={auth_code}&state=xyz"
    return RedirectResponse(url=redirect_url, status_code=302)
