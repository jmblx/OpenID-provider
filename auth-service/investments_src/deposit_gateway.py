from typing import Any


class DepositGateway:
    def get_deposits(self) -> dict[str, dict[str, Any]]:
        return {
            "Вклад «Премиальный»": {
                "min_value": 1000000,
                "max_value": 50000000,
                "year_percent": 22,
            },
            "Вклад «Новогодний»": {
                "min_value": 250000,
                "max_value": 999999,
                "year_percent": 18,
            },
            "Вклад «Универсальный»": {
                "min_value": 25000,
                "max_value": 24999,
                "year_percent": 16,
            },
        }
