from abc import abstractmethod, ABC
from dataclasses import dataclass
from uuid import UUID

from domain.entities.user.value_objects import UserID


@dataclass
class UserStrategyDTO:
    strategy_id: UUID
    budget: float
    days_duration: int
    portfolio: dict[str, float]
    current_balance: float
    start_date: str
    end_date: str


@dataclass
class UserStrategiesDTO:
    user_id: UUID
    strategies: list[UserStrategyDTO]


class UserReader(ABC):
    @abstractmethod
    async def get_user_strategies_by_id(self, user_id: UserID) -> UserStrategiesDTO: ...

