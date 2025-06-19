from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from starlette import status

from application.common.auth_server_token_types import AuthServerTokens
from application.third_party_auth.yandex.login_handler import (
    YandexLoginCommand,
    YandexLoginHandler,
)
from application.third_party_auth.yandex.register_handler import (
    YandexRegisterCommand,
    YandexRegisterHandler,
)
from presentation.web_api.manage_tokens import (
    change_active_account,
    set_auth_server_tokens,
)

third_party_router = APIRouter(
    route_class=DishkaRoute, tags=["third-party-providers"]
)


@third_party_router.post("/login/yandex")
async def login_with_yandex(
    handler: FromDishka[YandexLoginHandler],
    command: YandexLoginCommand,
    prev_account_tokens: FromDishka[AuthServerTokens],
) -> ORJSONResponse:
    new_jwt_tokens, prev_active_account_id, new_active_user_id = (
        await handler.handle(command)
    )
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
            str(new_active_user_id.value),
        )
    else:
        set_auth_server_tokens(response, new_jwt_tokens)
    return response


@third_party_router.post("/register/yandex")
async def register_with_yandex(
    handler: FromDishka[YandexRegisterHandler], command: YandexRegisterCommand
):
    register_handler_response = await handler.handle(command)
    response = ORJSONResponse(
        {"id": register_handler_response["user_id"]},
        status_code=status.HTTP_201_CREATED,
    )
    set_auth_server_tokens(response, register_handler_response)
    return response
