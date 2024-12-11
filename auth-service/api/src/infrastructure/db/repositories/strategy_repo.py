from datetime import date, timedelta
from uuid import UUID

from sqlalchemy import insert, update, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.strategy.model import Strategy
from domain.entities.user.value_objects import UserID
from infrastructure.db.models.secondary import user_strategy_association_table


class StrategyRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, strategy: Strategy, portfolio: dict, user_id: UserID) -> UUID:
        # Проверяем, существует ли ассоциация с таким strategy_id и user_id
        stmt = select(user_strategy_association_table).filter(
            user_strategy_association_table.c.strategy_id == strategy.id,
            user_strategy_association_table.c.user_id == user_id.value
        )
        result = await self.session.execute(stmt)
        existing_association = result.scalars().first()

        if existing_association:
            return existing_association.id  # Возвращаем существующий ID, если ассоциация уже существует

        # Если ассоциации нет, создаем новую
        self.session.add(strategy)
        await self.session.flush()

        start_date = date.today()
        end_date = start_date + timedelta(days=strategy.days_duration)

        current_balance = strategy.calculate_balance(portfolio)

        stmt = insert(user_strategy_association_table).values(
            user_id=user_id.value,
            strategy_id=strategy.id,
            portfolio=portfolio,  # Портфель передается как словарь
            current_balance=current_balance,
            start_date=start_date,
            end_date=end_date,
            in_process=True
        ).returning(user_strategy_association_table.c.id)

        await self.session.execute(stmt)
        return strategy.id

    async def get_by_id(self, id: UUID) -> Strategy | None:
        return await self.session.get(Strategy, id)

    async def update_user_portfolio(self, strategy_id: UUID, user_id: UUID, portfolio: dict) -> None:
        """Обновление портфеля пользователя для стратегии"""
        stmt = update(user_strategy_association_table).where(and_(
            user_strategy_association_table.c.strategy_id == strategy_id,
            user_strategy_association_table.c.user_id == user_id
        )).values(
            portfolio=portfolio["portfolio"],
            current_balance=portfolio["current_balance"]
        )

        await self.session.execute(stmt)

    async def get_user_portfolio(self, strategy_id: UUID, user_id: UUID) -> dict:
        stmt = select(user_strategy_association_table).where(and_(
            user_strategy_association_table.c.strategy_id == strategy_id,
            user_strategy_association_table.c.user_id == user_id
        ))
        result = await self.session.execute(stmt)
        record = result.scalar_one_or_none()

        if not record:
            raise ValueError(f"Портфель пользователя {user_id} для стратегии {strategy_id} не найден.")

        return {
            "portfolio": record.portfolio,
            "current_balance": record.current_balance
        }
