from dataclasses import dataclass, field
from uuid import UUID

from domain.entities.user.model import User


@dataclass
class Strategy:
    id: UUID = field(init=False)
    budget: float
    days_duration: int
    users: list[User] = field(default_factory=list)

    @classmethod
    def create(cls, budget: float, days_duration: int) -> "Strategy":
        return cls(
            budget=budget,
            days_duration=days_duration,
        )

    def add_user(self, user: User) -> None:
        """Метод для добавления пользователей в стратегию"""
        self.users.append(user)

    def calculate_balance(self, portfolio: dict) -> float:
        total_value = self.budget

        for asset_type, assets in portfolio.items():
            for asset in assets:
                if 'quantity' in asset:
                    total_value += asset['quantity']
        return total_value

