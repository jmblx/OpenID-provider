from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from starlette import status

from application.auth.code_to_token_handler import (
    CodeToTokenHandler,
    CodeToTokenCommand,
)
from application.auth.login_user_handler import (
    AuthenticateUserHandler,
    AuthenticateUserCommand,
)
from application.common.token_types import Fingerprint
from presentation.web_api.utils import render_auth_code_url

auth_router = APIRouter(route_class=DishkaRoute, tags=["auth"])
# jinja_loader = PackageLoader("presentation.web_api.registration")
# templates = Jinja2Templates(directory="templates", loader=jinja_loader)


@auth_router.post("/login")
async def login(
    command: AuthenticateUserCommand,
    handler: FromDishka[AuthenticateUserHandler],
) -> ORJSONResponse:
    auth_code = await handler.handle(command)
    redirect_url = render_auth_code_url(command.redirect_url, auth_code)
    return ORJSONResponse(
        {"redirect_url": redirect_url}, status_code=status.HTTP_201_CREATED
    )


@auth_router.post("/code-to-token")
async def code_to_token(
    handler: FromDishka[CodeToTokenHandler],
    fingerprint: FromDishka[Fingerprint],
    command: CodeToTokenCommand,
) -> ORJSONResponse:
    access_token, refresh_token = await handler.handle(command, fingerprint)
    response = ORJSONResponse(
        # {"access_token": access_token, "refresh_token": refresh_token},
        {"status": "success"},
        status_code=status.HTTP_200_OK,
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        max_age=60 * 5,
        expires=60 * 5,
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


# @auth_router.get("/pages/login")
# async def login_page(  # type: ignore
#         data: Annotated[UserAuthRequest, Param()],
#         client_service: FromDishka[ClientService],
#         request: Request,
# ):
#     client = await client_service.get_validated_client(data)
#     return templates.TemplateResponse(
#         "login.html",
#         convert_request_to_render(client, data, request),
#     )
