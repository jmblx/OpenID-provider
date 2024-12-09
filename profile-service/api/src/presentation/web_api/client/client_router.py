from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi.params import Param
from fastapi.responses import ORJSONResponse

from application.client.commands.register_client_command import (
    RegisterClientCommand,
)
from application.client.commands.validate_client_request import ValidateClientRequest
from application.client.handlers.register_client_hadler import (
    RegisterClientHandler,
)
from application.client.queries.client_queries import ClientAuthValidationQueryHandler, ClientAuthResponse
from application.dtos.client import ClientCreateDTO
from presentation.web_api.client.models import ClientAuthResponseModel

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
    client_data: ClientAuthResponse = await handler.handle(data)
    return ORJSONResponse(client_data)
