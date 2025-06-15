import logging
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Request
from fastapi.responses import ORJSONResponse
from starlette import status

from application.auth_as.get_available_accounts_query import GetAvailableAccountsHandler, GetAvailableAccountsResponse, \
    GetAvailableAccountsQuery
from application.auth_as.login_user_auth_server import (
    AuthenticateUserCommand,
    LoginUserHandler,
)
from application.auth_for_client.code_to_token_handler import CodeToTokenHandler, CodeToTokenCommand
from application.auth_for_client.get_me_page_data_handler import GetMeDataHandler, GetMeDataCommand, MeData
from application.common.auth_server_token_types import AuthServerTokens, AuthServerRefreshToken, NonActiveRefreshTokens, \
    AuthServerAccessToken
from application.common.id_provider import UserIdentityProvider
from presentation.web_api.routes.auth.models import GetMePageDataSchema, NewActiveUserSchema
from presentation.web_api.manage_tokens import set_auth_server_tokens, set_client_tokens, change_active_account, \
    get_tokens_by_user_id, deactivate_account_tokens, activate_account

auth_router = APIRouter(route_class=DishkaRoute, tags=["auth"])
# jinja_loader = PackageLoader("presentation.web_api.registration")
# templates = Jinja2Templates(directory="templates", loader=jinja_loader)


logger = logging.getLogger(__name__)


@auth_router.post("/login")
async def login(
    command: AuthenticateUserCommand,
    handler: FromDishka[LoginUserHandler],
    prev_account_tokens: FromDishka[AuthServerTokens],
) -> ORJSONResponse:
    new_jwt_tokens, prev_active_account_id, new_active_user_id = await handler.handle(command)
    response = ORJSONResponse(
        {"status": "success"},
        status_code=status.HTTP_200_OK,
    )
    if prev_active_account_id:
        change_active_account(
            response,
            str(prev_active_account_id.value),
            prev_account_tokens,
            new_jwt_tokens,
            str(new_active_user_id.value)
        )
    else:
        set_auth_server_tokens(response, new_jwt_tokens)
    return response


@auth_router.post("/code-to-token")
async def code_to_token(
    handler: FromDishka[CodeToTokenHandler],
    command: CodeToTokenCommand,
) -> ORJSONResponse:
    response_data = await handler.handle(command)
    tokens = {
        "access_token": response_data.pop("access_token", None),
        "refresh_token": response_data.pop("refresh_token", None),
    }

    response = ORJSONResponse(content={"status": "success"}, status_code=status.HTTP_200_OK)

    set_client_tokens(response, tokens)

    return response


@auth_router.post("/auth-to-client")
async def auth_to_client(handler: FromDishka[GetMeDataHandler], command: GetMePageDataSchema) -> MeData:
    command_data = GetMeDataCommand(
        client_id=command.client_id,
        required_resources=command.required_resources.model_dump(),  # TypedDict из Pydantic-модели
        redirect_url=str(command.redirect_url),
        code_verifier=command.code_verifier,
        code_challenge_method=command.code_challenge_method,
    )
    return await handler.handle(command_data)


@auth_router.post("/switch-account")
async def switch_account(
    idp: FromDishka[UserIdentityProvider],
    prev_account_tokens: FromDishka[AuthServerTokens],
    new_active_user: NewActiveUserSchema,
    request: Request,
) -> ORJSONResponse:
    prev_active_user_id = await idp.get_current_user_id()
    if new_active_user.new_active_user_id == prev_active_user_id:
        raise status.HTTP_409_CONFLICT("accounts are the same")
    response = ORJSONResponse(content={"status": "success"}, status_code=status.HTTP_200_OK)
    change_active_account(
        response,
        str(prev_active_user_id.value),
        prev_account_tokens,
        get_tokens_by_user_id(request, str(new_active_user.new_active_user_id)),
        str(new_active_user.new_active_user_id)
    )
    return response


@auth_router.get("/available-accounts")
async def get_available_accounts(
    handler: FromDishka[GetAvailableAccountsHandler],
    non_active_tokens: FromDishka[NonActiveRefreshTokens]
) -> GetAvailableAccountsResponse:
    return await handler.handle(GetAvailableAccountsQuery(non_active_tokens))

@auth_router.post("/deactivate-current-account")
async def deactivate_account(
    idp: FromDishka[UserIdentityProvider],
    prev_account_tokens: FromDishka[AuthServerTokens],
):
    response = ORJSONResponse(content={"status": "success"}, status_code=status.HTTP_200_OK)
    deactivate_account_tokens(response, str((await idp.get_current_user_id()).value), prev_account_tokens)
    return response


@auth_router.post("/activate-account")
async def activate_account_tokens(
    new_active_user: NewActiveUserSchema,
    request: Request,
) -> ORJSONResponse:
    response = ORJSONResponse(content={"status": "success"}, status_code=status.HTTP_200_OK)
    new_active_user_tokens = get_tokens_by_user_id(request, str(new_active_user.new_active_user_id))
    if not new_active_user_tokens:
        raise status.HTTP_404_NOT_FOUND("there is no account with such id in your non-active accounts")
    activate_account(
        response,
        str(new_active_user),
        new_active_user_tokens,
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
