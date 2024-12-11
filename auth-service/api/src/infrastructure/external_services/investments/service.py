import json
from datetime import datetime, timedelta, date
from typing import List, Dict

import pytz
import redis.asyncio as aioredis

class InvestmentsService:
    def __init__(self, redis: aioredis.Redis):
        self.redis = redis

    async def get_investments(self) -> dict[str, dict]:
        investments = await self.redis.get("data")
        return json.loads(investments)

    def get_price_change_percentage(self, old_price: float, new_price: float) -> float:
        """Вычисляем процентное изменение цены"""
        return ((new_price - old_price) / old_price) * 100

    async def check_for_significant_changes(self, portfolio: dict, threshold: float = 5.0) -> List[str]:
        """Проверка изменений в портфеле за последние 7 дней"""
        notifications = []
        investments = await self.get_investments()
        today = datetime.today().strftime("%d.%m.%Y")
        seven_days_ago = (datetime.today() - timedelta(days=7)).strftime("%d.%m.%Y")

        # Проверяем акции, облигации, валюты и золото
        for investment_type, data in portfolio.items():
            if investment_type not in investments:
                continue
            print(investment_type, data)
            # Для каждого актива проверяем изменения
            for asset in data:
                asset_name = asset["name"]
                quantity = asset["quantity"]
                price_history = investments[investment_type]

                if seven_days_ago in price_history and today in price_history:
                    old_price = float(price_history[seven_days_ago].get("price", 0).replace("₽", "").replace(",", "."))
                    new_price = float(price_history[today].get("price", 0).replace("₽", "").replace(",", "."))
                    price_change = self.get_price_change_percentage(old_price, new_price)

                    if abs(price_change) >= threshold:
                        notifications.append(f"Актив {asset_name} изменил свою цену на {price_change:.2f}% за неделю (текущая цена: {new_price} ₽).")

                if today in price_history:
                    next_7_day_diff = price_history[today].get("next_7_day_diff_in_%", "0")
                    next_7_day_diff = float(next_7_day_diff.replace("%", ""))
                    if abs(next_7_day_diff) >= threshold:
                        notifications.append(f"Прогноз на актив {asset_name}: изменение цены на {next_7_day_diff:.2f}% за следующие 7 дней.")
                try:
                    print(today, price_history, next_7_day_diff, price_change)
                except Exception as e:
                    print(e)
        return notifications

    async def check_strategy_end_date(self, end_date: str) -> List[str]:
        """Проверка, если до окончания стратегии осталось менее 7 дней"""
        notifications = []
        today = datetime.today().date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        if end_date - today <= timedelta(days=7):
            notifications.append("Стратегия заканчивается через 7 дней или меньше. Убедитесь, что вы готовы.")

        return notifications

    async def get_price_by_date_and_name(self, asset_type: str, asset_name: str) -> float:
        investments = await self.get_investments()

        # Получаем текущую дату по Москве
        today = date.today().strftime("%d.%m.%Y")

        if asset_type not in investments:
            raise ValueError(f"Неизвестный тип актива: {asset_type}")

        asset_data = investments[asset_type]

        if today not in asset_data:
            raise ValueError(f"Данные по дате {today} не найдены для актива {asset_name}")

        asset_price_data = asset_data[today]

        if asset_name not in asset_price_data:
            raise ValueError(f"Цена для актива {asset_name} не найдена на дату {today}")

        price = asset_price_data[asset_name]["price"]

        price = float(price.replace("₽", "").replace(",", "."))

        return price
