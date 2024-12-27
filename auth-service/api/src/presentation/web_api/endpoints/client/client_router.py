from typing import Annotated
from urllib.parse import unquote

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi.params import Param
from fastapi.responses import ORJSONResponse
from starlette.status import HTTP_204_NO_CONTENT

from application.client.add_allowed_redirect_url.add_allowed_url import AddAllowedRedirectUrlCommand, \
    AddAllowedRedirectUrlCommandHandler
from application.client.get_client.client_queries import ValidateClientRequest, ClientAuthValidationQueryHandler, \
    ClientAuthResponse
from application.client.register_client.register_client_hadler import (
    RegisterClientHandler, RegisterClientCommand,
)
from application.client.rename_client.rename_client import (
    RenameClientCommand,
    RenameClientCommandHandler,
)
from application.dtos.client import ClientCreateDTO
from presentation.web_api.endpoints.client.models import ClientAuthResponseModel

client_router = APIRouter(prefix="/client", route_class=DishkaRoute)


@client_router.post("/")
async def create_client(
    command: RegisterClientCommand, handler: FromDishka[RegisterClientHandler]
) -> ClientCreateDTO:
    client = await handler.handle(command)
    return client


@client_router.get("/auth", response_model=ClientAuthResponseModel)
async def register_page(
    data: Annotated[ValidateClientRequest, Param()],
    handler: FromDishka[ClientAuthValidationQueryHandler],
) -> ORJSONResponse:
    data.redirect_url = unquote(data.redirect_url)
    client_data: ClientAuthResponse = await handler.handle(data)
    return ORJSONResponse(client_data)


@client_router.patch("/{client_id}/rename")
async def rename_client(
    client_id: int,
    command: RenameClientCommand,
    handler: FromDishka[RenameClientCommandHandler],
) -> ORJSONResponse:
    await handler.handle(command=command, client_id=client_id)
    return ORJSONResponse({"status": "success"}, status_code=HTTP_204_NO_CONTENT)


@client_router.patch("/{client_id}/add_redirect_url")
async def add_allowed_redirect_url(
    client_id: int,
    command: AddAllowedRedirectUrlCommand,
    handler: FromDishka[AddAllowedRedirectUrlCommandHandler],
) -> ORJSONResponse:
    await handler.handle(command=command, client_id=client_id)
    return ORJSONResponse({"status": "success"}, status_code=HTTP_204_NO_CONTENT)
