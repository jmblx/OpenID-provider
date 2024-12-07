from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from starlette.status import HTTP_200_OK

from application.auth.handlers.refresh_tokens_handler import RefreshTokensHandler
from application.auth.handlers.revoke_tokens_handler import RevokeTokensHandler
from application.auth.token_types import RefreshToken, Fingerprint

token_manage_router = APIRouter(route_class=DishkaRoute, tags=["token-manage"])


@token_manage_router.post("/refresh")
async def refresh_token(
    refresh_token: FromDishka[RefreshToken],
    fingerprint: FromDishka[Fingerprint],
    handler: FromDishka[RefreshTokensHandler],
) -> ORJSONResponse:
    access_token, new_refresh_token = await handler.handle(refresh_token, fingerprint)
    response = ORJSONResponse({"detail": "Tokens refreshed successfully"})
    response.set_cookie("refresh_token", new_refresh_token)
    response.set_cookie("access_token", access_token)
    response.status_code = HTTP_200_OK
    return response


@token_manage_router.post("/revoke")
async def revoke_token(
    refresh_token: FromDishka[RefreshToken], handler: FromDishka[RevokeTokensHandler]
) -> ORJSONResponse:
    await handler.handle(refresh_token)
    response = ORJSONResponse({"detail": "Tokens revoked successfully"})
    response.delete_cookie("refresh_token")
    response.delete_cookie("access_token")
    response.status_code = HTTP_200_OK
    return response
