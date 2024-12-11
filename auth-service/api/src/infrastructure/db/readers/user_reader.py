from sqlalchemy import text

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
        # Запрос для получения стратегий пользователя через ассоциативную таблицу
        query = text("""
            SELECT strategy.id, strategy.budget, strategy.days_duration,
                   user_strategy_association.portfolio, 
                   user_strategy_association.current_balance,
                   user_strategy_association.start_date, 
                   user_strategy_association.end_date
            FROM strategy
            JOIN user_strategy_association
                ON strategy.id = user_strategy_association.strategy_id
            WHERE user_strategy_association.user_id = :user_id
        """)

        result = await self.session.execute(query, {"user_id": user_id.value})
        strategies = result.fetchall()

        if not strategies:
            raise ValueError(f"Стратегии для пользователя {user_id.value} не найдены.")

        # Заполняем DTO с данными по стратегиям
        user_strategies = []
        for strategy in strategies:
            strategy_data = strategy  # В данной строке данные о стратегии

            # Заполняем DTO для каждой стратегии
            user_strategies.append(UserStrategyDTO(
                strategy_id=strategy_data[0],
                budget=strategy_data[1],
                days_duration=strategy_data[2],
                portfolio=strategy_data[3],
                current_balance=strategy_data[4],
                start_date=strategy_data[5].strftime('%Y-%m-%d'),
                end_date=strategy_data[6].strftime('%Y-%m-%d')
            ))

        return UserStrategiesDTO(user_id=user_id.value, strategies=user_strategies)

    async def _get_user_strategy_association(self, strategy_id: UUID, user_id: UserID):
        # Полный запрос для получения ассоциативной записи для пользователя и стратегии
        query = text("""
            SELECT user_strategy_association.id, 
                   user_strategy_association.strategy_id, 
                   user_strategy_association.user_id, 
                   user_strategy_association.portfolio, 
                   user_strategy_association.current_balance, 
                   user_strategy_association.start_date, 
                   user_strategy_association.end_date
            FROM user_strategy_association
            WHERE user_strategy_association.strategy_id = :strategy_id 
              AND user_strategy_association.user_id = :user_id
        """)

        result = await self.session.execute(query, {"strategy_id": strategy_id, "user_id": user_id.value})

        user_strategy = result.fetchall()

        if not user_strategy:
            raise ValueError(f"Association not found for user {user_id.value} and strategy {strategy_id}")

        user_strategy = user_strategy[0]

        return user_strategy
