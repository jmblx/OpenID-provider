from typing import Any

from application.common.id_provider import IdentityProvider
from domain.exceptions.user import UnauthenticatedUserError
from infrastructure.external_services.investments.service import InvestmentsService


class InvestmentsQueryHandler:
    def __init__(
        self, id_provider: IdentityProvider, investments_service: InvestmentsService
    ):
        self.id_provider = id_provider
        self.investments_service = investments_service

    async def handle(self) -> dict[str, Any]:
        user_id = self.id_provider.get_current_user_id()
        if not user_id:
            raise UnauthenticatedUserError()
        return await self.investments_service.get_investments()
