from dataclasses import dataclass
from uuid import UUID

from application.common.id_provider import IdentityProvider
from application.common.uow import Uow
from application.common.interfaces.user_repo import UserRepository
from infrastructure.db.repositories.strategy_repo import StrategyRepo
from infrastructure.external_services.investments.service import InvestmentsService


@dataclass
class BuyItemCommand:
    strategy_id: UUID
    asset_name: str
    asset_type: str
    quantity: float
    date: str



class BuyInvestmentHandler:
    def __init__(self, investment_service: InvestmentsService, user_repo: UserRepository, strategy_repo: StrategyRepo, id_provider: IdentityProvider, uow: Uow) -> None:
        self.id_provider = id_provider
        self.investment_service = investment_service
        self.user_repo = user_repo
        self.strategy_repo = strategy_repo
        self.uow = uow

    async def handle(self, command: BuyItemCommand) -> float:
        price = await self.investment_service.get_price_by_date_and_name(
            asset_type=command.asset_type,
            asset_name=command.asset_name
        )

        total_cost = price * command.quantity

        strategy = await self.strategy_repo.get_by_id(command.strategy_id)

        user = await self.user_repo.get_by_id(self.id_provider.get_current_user_id())

        portfolio = await self.strategy_repo.get_user_portfolio(strategy.id, user.id.value)

        if portfolio["current_balance"] < total_cost:
            raise ValueError("Недостаточно средств для покупки.")

        if command.asset_name in portfolio["portfolio"]:
            portfolio["portfolio"][command.asset_name]["quantity"] += command.quantity
        else:
            portfolio["portfolio"][command.asset_name] = {
                "name": command.asset_name,
                "quantity": command.quantity
            }

        portfolio["current_balance"] -= total_cost

        await self.strategy_repo.update_user_portfolio(strategy.id, user.id.value, portfolio)
        await self.uow.commit()
        return portfolio["current_balance"]
