from fastapi import APIRouter

from application.auth.commands.register_client_command import RegisterClientCommand
from application.auth.handlers.register_client_hadler import RegisterClientHandler
from application.dtos.client import ClientCreateDTO

client_router = APIRouter(prefix="/client")

@client_router.post("/")
async def create_client(command: RegisterClientCommand, handler: RegisterClientHandler) -> ClientCreateDTO:
    client = await handler.handle(command)
    return client
