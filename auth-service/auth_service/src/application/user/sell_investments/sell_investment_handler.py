from uuid import UUID
from dataclasses import dataclass

from application.common.uow import Uow
from infrastructure.external_services.investments.service import (
    InvestmentsService,
)
from application.common.interfaces.user_repo import UserRepository
from infrastructure.db.repositories.strategy_repo import StrategyRepo
from application.common.id_provider import IdentityProvider


@dataclass
class SellItemCommand:
    strategy_id: UUID
    asset_name: str
    asset_type: str
    quantity: float
    date: str


class SellInvestmentHandler:
    def __init__(
        self,
        investment_service: InvestmentsService,
        user_repo: UserRepository,
        strategy_repo: StrategyRepo,
        id_provider: IdentityProvider,
        uow: Uow,
    ):
        self.id_provider = id_provider
        self.investment_service = investment_service
        self.user_repo = user_repo
        self.strategy_repo = strategy_repo
        self.uow = uow

    async def handle(self, command: SellItemCommand) -> float:
        price = await self.investment_service.get_price_by_date_and_name(
            asset_type=command.asset_type,
            asset_name=command.asset_name,
        )

        total_revenue = price * command.quantity

        strategy = await self.strategy_repo.get_by_id(command.strategy_id)
        user = await self.user_repo.get_by_id(
            self.id_provider.get_current_user_id()
        )

        portfolio = await self.strategy_repo.get_user_portfolio(
            strategy.id, user.id.value
        )

        if command.asset_name not in portfolio["portfolio"]:
            raise ValueError(
                f"Актив {command.asset_name} не найден в портфеле."
            )

        if (
            portfolio["portfolio"][command.asset_name]["quantity"]
            < command.quantity
        ):
            raise ValueError(f"Недостаточно {command.asset_name} для продажи.")

        portfolio["portfolio"][command.asset_name][
            "quantity"
        ] -= command.quantity

        if portfolio["portfolio"][command.asset_name]["quantity"] == 0:
            del portfolio["portfolio"][command.asset_name]

        portfolio["current_balance"] += total_revenue

        await self.strategy_repo.update_user_portfolio(
            strategy.id, user.id.value, portfolio
        )
        await self.uow.commit()
        return portfolio["current_balance"]
