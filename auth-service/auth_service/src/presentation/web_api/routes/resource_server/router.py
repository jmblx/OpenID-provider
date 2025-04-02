from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from starlette import status
from starlette.responses import Response

from application.resource_server.read_rs_view_handler import ReadResourceServerPageViewQueryHandler, \
    ReadResourceServerPageViewQuery
from application.resource_server.register_rs_handler import RegisterResourceServerCommand, \
    RegisterResourceServerHandler
from application.resource_server.dtos import ResourceServerCreateDTO
from application.resource_server.update_rs_handler import UpdateResourceServerHandler, UpdateResourceServerCommand
from domain.entities.resource_server.value_objects import ResourceServerType
from presentation.web_api.routes.resource_server.models import ResourceServerViewModel

rs_router = APIRouter(route_class=DishkaRoute, tags=["resource_server"], prefix="/rs")

@rs_router.post("/")
async def register_rs(
    command: RegisterResourceServerCommand,
    handler: FromDishka[RegisterResourceServerHandler],
    response: Response
) -> ResourceServerCreateDTO:
    response.status_code = status.HTTP_201_CREATED
    rs = await handler.handle(command)
    return rs


class UpdateResourceServerModel(BaseModel):
    new_name: str | None
    new_type: ResourceServerType | None


@rs_router.put("/{rs_id}")
async def update_rs(
    rs_id: int,
    command: UpdateResourceServerModel,
    handler: FromDishka[UpdateResourceServerHandler],
) -> ORJSONResponse:
    command = UpdateResourceServerCommand(rs_id=rs_id, **command.model_dump())
    await handler.handle(command)
    return ORJSONResponse(
        {"status": "success"}, status_code=status.HTTP_200_OK
    )

@rs_router.get("/{rs_id}")
async def get_rs(
    rs_id: int, handler: FromDishka[ReadResourceServerPageViewQueryHandler]
) -> ResourceServerViewModel:
    rs_view = await handler.handle(
        ReadResourceServerPageViewQuery(rs_id=rs_id)
    )
    return ResourceServerViewModel(**rs_view)
