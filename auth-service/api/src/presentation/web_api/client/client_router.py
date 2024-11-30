from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends

from application.auth.commands.register_client_command import (
    RegisterClientCommand,
)
from application.auth.handlers.register_client_hadler import (
    RegisterClientHandler,
)
from application.dtos.client import ClientCreateDTO

client_router = APIRouter(prefix="/client", route_class=DishkaRoute)


@client_router.post("/")
async def create_client(
    command: RegisterClientCommand, handler: FromDishka[RegisterClientHandler]
) -> ClientCreateDTO:
    client = await handler.handle(command)
    return client
