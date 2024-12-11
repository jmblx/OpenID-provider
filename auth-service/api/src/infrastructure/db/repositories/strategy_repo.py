from datetime import date, timedelta
from uuid import UUID

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.strategy.model import Strategy
from infrastructure.db.models.secondary import user_strategy_association_table


class StrategyRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, strategy: Strategy, portfolio: dict) -> UUID:
        self.session.add(strategy)

        start_date = date.today()

        end_date = start_date + timedelta(days=strategy.days_duration)

        current_balance = strategy.calculate_balance(portfolio)

        user_id = strategy.users[0].id

        stmt = insert(user_strategy_association_table).values(
            user_id=user_id,
            strategy_id=strategy.id,
            portfolio=portfolio,
            current_balance=current_balance,
            start_date=start_date,
            end_date=end_date,
        )
        await self.session.execute(stmt)
        await self.session.commit()

        return strategy.id
