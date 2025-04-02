from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from application.auth_as.admin_login_handler import LoginAdminCommand, LoginAdminOtherTokensHandler

admin_router = APIRouter(route_class=DishkaRoute, tags=["resource_server"], prefix="/admin")


@admin_router.post("/login/admin")
async def login_admin(command: LoginAdminCommand, handler: LoginAdminOtherTokensHandler) -> ORJSONResponse:
    session_id = await handler.handle(command)
    return ORJSONResponse({"session_id": str(session_id)})
