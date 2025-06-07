from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from starlette import status

from application.third_party_auth.yandex.login_handler import YandexLoginCommand, YandexLoginHandler
from application.third_party_auth.yandex.register_handler import YandexRegisterCommand, YandexRegisterHandler
from presentation.web_api.response_token import set_auth_server_tokens

third_party_router = APIRouter(route_class=DishkaRoute, tags=["third-party-providers"])

@third_party_router.post("/login/yandex")
async def login_with_yandex(handler: FromDishka[YandexLoginHandler], command: YandexLoginCommand) -> ORJSONResponse:
    tokens = await handler.handle(command)
    response = ORJSONResponse(
        # {"access_token": access_token, "refresh_token": refresh_token},
        {"status": "success"},
        status_code=status.HTTP_200_OK,
    )
    set_auth_server_tokens(response, tokens)
    return response


@third_party_router.post("/register/yandex")
async def register_with_yandex(handler: FromDishka[YandexRegisterHandler], command: YandexRegisterCommand):
    register_handler_response = await handler.handle(command)
    response = ORJSONResponse(
        {"id": register_handler_response["user_id"]},
        status_code=status.HTTP_201_CREATED,
    )
    set_auth_server_tokens(response, register_handler_response)
    return response
