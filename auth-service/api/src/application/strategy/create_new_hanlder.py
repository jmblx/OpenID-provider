from dataclasses import dataclass
from typing import Any
from uuid import UUID

from application.common.id_provider import IdentityProvider
from application.common.uow import Uow
from application.user.interfaces.repo import UserRepository
from domain.entities.strategy.model import Strategy
from domain.exceptions.user import UnauthenticatedUserError
from infrastructure.db.repositories.strategy_repo import StrategyRepo

@dataclass
class CreateNewStrategyCommand:
    budget: float
    days_duration: int
    portfolio: dict[str, Any]


class CreateNewStrategyHanlder:
    def __init__(self, strategy_repo: StrategyRepo, uow: Uow, user_repo: UserRepository, idp: IdentityProvider):
        self.strategy_repo = strategy_repo
        self.uow = uow
        self.user_repo = user_repo
        self.idp = idp

    async def handle(self, command: CreateNewStrategyCommand) -> UUID:
        user_id = self.idp.get_current_user_id()
        if not user_id:
            raise UnauthenticatedUserError()

        strategy = Strategy.create(command.budget, command.days_duration)

        user = await self.user_repo.by_id(user_id)
        strategy.add_user(user)

        strategy_id = await self.strategy_repo.save(strategy, command.portfolio)
        await self.uow.commit()
        return strategy_id
