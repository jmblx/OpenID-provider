import json
from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.entities.strategy.model import Strategy
from domain.entities.user.value_objects import UserID
from infrastructure.db.models.secondary import user_strategy_association_table


@dataclass
class ReadStrategyDTO:
    strategy_id: UUID
    budget: float
    days_duration: int
    portfolio: dict[str, float] | None
    user_id: UUID
    current_balance: float
    start_date: str
    end_date: str


class StrategyReader:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def read_by_id(self, strategy_id: UUID, user_id: UserID) -> ReadStrategyDTO:
        query = (
            select(Strategy)
            .options(selectinload(Strategy.users))
            .filter(Strategy.id == strategy_id)
        )

        result = await self.session.execute(query)
        strategy = result.scalars().first()

        if not strategy:
            raise ValueError("Стратегия не найдена")

        user_strategy = await self._get_user_strategy_association(strategy_id, user_id)

        current_balance = strategy.calculate_balance(user_strategy.portfolio)

        return ReadStrategyDTO(
            strategy_id=strategy.id,
            budget=strategy.budget,
            days_duration=strategy.days_duration,
            portfolio=user_strategy.portfolio,
            user_id=user_id.value,
            current_balance=current_balance,
            start_date=user_strategy.start_date.strftime('%d.%m.%Y'),  # в формате '05.12.2024'
            end_date = user_strategy.end_date.strftime('%d.%m.%Y')  # в формате '06.12.2024'

        )

    async def _get_user_strategy_association(self, strategy_id: UUID, user_id: UserID):
        query = select(
            user_strategy_association_table.c.id,  # если нужен id
            user_strategy_association_table.c.strategy_id,
            user_strategy_association_table.c.user_id,
            user_strategy_association_table.c.portfolio,
            user_strategy_association_table.c.current_balance,
            user_strategy_association_table.c.start_date,
            user_strategy_association_table.c.end_date
        ).where(and_(
            user_strategy_association_table.c.strategy_id == strategy_id,
            user_strategy_association_table.c.user_id == user_id.value
        ))

        result = await self.session.execute(query)

        # Получаем все строки
        user_strategy = result.fetchall()

        # Если результат пустой, выбрасываем исключение
        if not user_strategy:
            raise ValueError(
                f"User strategy association for user {user_id.value} and strategy {strategy_id} not found.")

        # Теперь можно работать с результатом
        user_strategy = user_strategy[0]  # Берем первую строку

        # Проверяем, если portfolio None, то присваиваем пустой словарь
        portfolio = user_strategy.portfolio
        if portfolio is None:
            portfolio = {}

        print(f"User strategy data: {user_strategy}")

        return user_strategy
