import json
import logging
from datetime import datetime, timedelta, date
from typing import List, Dict

import pytz
import redis.asyncio as aioredis

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG
)  # Можно менять на INFO или ERROR в зависимости от нужд
logger = logging.getLogger(__name__)


class InvestmentsService:
    def __init__(self, redis: aioredis.Redis):
        self.redis = redis

    async def get_investments(self) -> dict[str, dict]:
        investments = await self.redis.get("data")
        investments_dict = json.loads(investments)
        return investments_dict

    async def get_price_by_date_and_name(
        self, asset_type: str, asset_name: str
    ) -> float:
        investments = await self.get_investments()
        today = date.today().strftime("%d.%m.%Y")

        print(
            f"Получение цены для актива {asset_name} типа {asset_type} на дату {today}"
        )

        if asset_type not in investments:
            print(f"Неизвестный тип актива: {asset_type}")
            raise ValueError(f"Неизвестный тип актива: {asset_type}")

        asset_data = investments[asset_type]
        if today not in asset_data:
            print(f"Данные по дате {today} не найдены для актива {asset_name}")
            raise ValueError(
                f"Данные по дате {today} не найдены для актива {asset_name}"
            )

        asset_price_data = asset_data[today]
        if asset_name not in asset_price_data:
            print(f"Цена для актива {asset_name} не найдена на дату {today}")
            raise ValueError(
                f"Цена для актива {asset_name} не найдена на дату {today}"
            )

        price = asset_price_data[asset_name]["price"]
        price = float(price.replace("₽", "").replace(",", "."))
        print(f"Цена для {asset_name} на {today}: {price} ₽")
        return price
