from uuid import UUID

from application.common.id_provider import IdentityProvider
from domain.exceptions.user import UnauthenticatedUserError
from infrastructure.db.readers.strategy_reader import (
    StrategyReader,
    ReadStrategyDTO,
)


class StrategyQueryHandler:
    def __init__(
        self, strategy_reader: StrategyReader, idp: IdentityProvider
    ) -> None:
        self.strategy_reader = strategy_reader
        self.idp = idp

    async def handle(self, strategy_id: UUID) -> ReadStrategyDTO:
        user_id = self.idp.get_current_user_id()
        if not user_id:
            raise UnauthenticatedUserError()
        strategy = await self.strategy_reader.read_by_id(strategy_id, user_id)
        return strategy
