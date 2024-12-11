from application.user.interfaces.reader import UserReader, UserStrategiesDTO, UserStrategyDTO

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from domain.entities.strategy.model import Strategy
from domain.entities.user.value_objects import UserID
from infrastructure.db.models.secondary import user_strategy_association_table
from uuid import UUID


class UserReaderImpl(UserReader):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_strategies_by_id(self, user_id: UserID) -> UserStrategiesDTO:
        query = select(Strategy).join(
            user_strategy_association_table
        ).filter(
            user_strategy_association_table.c.user_id == user_id
        ).options(selectinload(Strategy.users))  # Загружаем ассоциированного пользователя

        result = await self.session.execute(query)
        strategies = result.scalars().all()

        # Заполняем DTO с данными по стратегиям
        user_strategies = []
        for strategy in strategies:
            user_strategy = await self._get_user_strategy_association(strategy.id, user_id)

            current_balance = strategy.calculate_balance(user_strategy.portfolio)  # Расчет баланса на основе портфеля

            user_strategies.append(UserStrategyDTO(
                strategy_id=strategy.id,
                budget=strategy.budget,
                days_duration=strategy.days_duration,
                portfolio=user_strategy.portfolio,
                current_balance=current_balance,
                start_date=user_strategy.start_date.strftime('%Y-%m-%d'),
                end_date=user_strategy.end_date.strftime('%Y-%m-%d')
            ))

        return UserStrategiesDTO(user_id=user_id.value, strategies=user_strategies)

    async def _get_user_strategy_association(self, strategy_id: UUID, user_id: UserID):
        # Запрос для получения ассоциативной записи для пользователя и стратегии
        query = select(user_strategy_association_table).filter_by(strategy_id=strategy_id, user_id=user_id)
        result = await self.session.execute(query)
        return result.scalars().first()

