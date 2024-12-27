from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from starlette.status import HTTP_201_CREATED

from application.create_role.create_role_handler import CreateRoleHandler, CreateRoleCommand

role_router = APIRouter(route_class=DishkaRoute, tags=["role"], prefix="/role")


@role_router.post("/")
async def create_role(
    command: CreateRoleCommand, handler: FromDishka[CreateRoleHandler]
) -> ORJSONResponse:
    role_id = await handler.handle(command)
    return ORJSONResponse({"role_id": role_id}, status_code=HTTP_201_CREATED)
