from typing import Annotated
from urllib.parse import unquote

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.params import Param
from fastapi.responses import ORJSONResponse
from starlette.status import HTTP_204_NO_CONTENT

from application.client.add_allowed_url import (
    AddAllowedRedirectUrlCommand,
    AddAllowedRedirectUrlCommandHandler,
)
from application.client.client_queries import (
    ValidateClientRequest,
    ClientAuthValidationQueryHandler,
    ClientAuthResponse,
)
from application.client.find_clients import FindClientsQuery, FindClientsHandler
from application.client.get_all_clients import GetClientsIdsHandler, GetClientsIdsQuery
from application.client.set_client_avatar_handler import SetClientAvatarHandler, SetClientAvatarCommand
from application.common.views.client_view import ClientsIdsData
from application.client.read_client_view_handler import (
    ReadClientPageViewQueryHandler,
    ReadClientPageViewQuery,
)
from application.client.register_client_hadler import (
    RegisterClientHandler,
    RegisterClientCommand,
)
from application.client.update_client import (
    UpdateClientCommand,
    UpdateClientCommandHandler,
)
from application.dtos.client import ClientCreateDTO
from application.dtos.set_image import ImageDTO
from domain.entities.client.value_objects import ClientID
from presentation.web_api.common.schemas import PaginationData
from presentation.web_api.routes.client.models import (
    ClientAuthResponseModel,
    ClientViewModel,
    UpdateClientModel,
)

client_router = APIRouter(prefix="/client", route_class=DishkaRoute, tags=["client"])


@client_router.post("")
async def create_client(
    command: RegisterClientCommand, handler: FromDishka[RegisterClientHandler]
) -> ClientCreateDTO:
    client = await handler.handle(command)
    return client


@client_router.get("/search")
async def search_client_by_input(
    search_input: str,
    handler: FromDishka[FindClientsHandler],
) -> dict[ClientID, ClientsIdsData]:
    return await handler.handle(FindClientsQuery(search_input=search_input))


@client_router.get("/auth", response_model=ClientAuthResponseModel)
async def register_page(
    data: Annotated[ValidateClientRequest, Param()],
    handler: FromDishka[ClientAuthValidationQueryHandler],
) -> ORJSONResponse:
    data.redirect_url = unquote(data.redirect_url)
    client_data: ClientAuthResponse = await handler.handle(data)
    return ORJSONResponse(client_data)


@client_router.put("/{client_id}")
async def update_client(
    client_id: int,
    command: UpdateClientModel,
    handler: FromDishka[UpdateClientCommandHandler],
) -> ORJSONResponse:
    data = command.model_dump()
    data.update({"client_id": client_id})
    command = UpdateClientCommand(**data)
    await handler.handle(command)
    return ORJSONResponse(
        {"status": "success"}, status_code=HTTP_204_NO_CONTENT
    )


@client_router.put("/{client_id}/add_redirect_url")
async def add_allowed_redirect_url(
    client_id: int,
    command: AddAllowedRedirectUrlCommand,
    handler: FromDishka[AddAllowedRedirectUrlCommandHandler],
) -> ORJSONResponse:
    await handler.handle(command=command, client_id=client_id)
    return ORJSONResponse(
        {"status": "success"}, status_code=HTTP_204_NO_CONTENT
    )


@client_router.get("/ids_data")
async def get_client_ids(
    handler: FromDishka[GetClientsIdsHandler],
    pagination_data: Annotated[PaginationData, Param()],
) -> dict[ClientID, ClientsIdsData]:
    query = GetClientsIdsQuery(
        after_id=pagination_data.after_id,
        page_size=pagination_data.page_size
    )
    client_ids_data = await handler.handle(query)
    return client_ids_data


@client_router.get("/{client_id}")
async def get_client(
    client_id: int, handler: FromDishka[ReadClientPageViewQueryHandler]
) -> ClientViewModel:
    client_view = await handler.handle(
        ReadClientPageViewQuery(client_id=client_id)
    )
    return ClientViewModel(**client_view)


@client_router.post("/{client_id}/avatar")
async def set_avatar(handler: FromDishka[SetClientAvatarHandler], client_id: int, file: UploadFile = File(...)) -> ORJSONResponse:
    if not file:
        raise HTTPException(status_code=400, detail="Файл не был передан")

    content = await file.read()

    image_dto = ImageDTO(
        content=content,
        content_type=file.content_type
    )
    avatar_path = await handler.handle(SetClientAvatarCommand(image=image_dto, client_id=client_id))

    return ORJSONResponse({"avatar_path": avatar_path})
