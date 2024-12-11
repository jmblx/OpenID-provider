import json
import logging
from datetime import datetime, timedelta, date
from typing import List, Dict

import pytz
import redis.asyncio as aioredis

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)  # Можно менять на INFO или ERROR в зависимости от нужд
logger = logging.getLogger(__name__)


class InvestmentsService:
    def __init__(self, redis: aioredis.Redis):
        self.redis = redis

    async def get_investments(self) -> dict[str, dict]:
        try:
            investments = await self.redis.get("data")
            investments_dict = json.loads(investments)
            return investments_dict

    def get_price_change_percentage(self, old_price: float, new_price: float) -> float:
        """Вычисляем процентное изменение цены"""
        if old_price == 0:
            logger.warning(f"Старая цена равна нулю, невозможно вычислить процентное изменение")
            return 0.0
        price_change = ((new_price - old_price) / old_price) * 100
        print(f"Изменение цены: {price_change}% (старое: {old_price}, новое: {new_price})")
        return price_change

    def parse_price(self, price_str: str) -> float:
        """Преобразует строку с ценой в число (удаляет валюту и заменяет запятую на точку)."""
        try:
            price_str = price_str.replace("₽", "").replace(",", ".").strip()
            parsed_price = float(price_str)
            print(f"Цена преобразована: {price_str} -> {parsed_price}")
            return parsed_price
        except ValueError as e:
            print(f"Ошибка при преобразовании цены {price_str}: {e}")
            raise

    def parse_percentage(self, percentage_str: str) -> float:
        """Преобразует строку с процентом в число."""
        try:
            percentage = float(percentage_str.replace("%", "").strip())
            print(f"Процент преобразован: {percentage_str} -> {percentage}")
            return percentage
        except ValueError as e:
            print(f"Ошибка при преобразовании процента {percentage_str}: {e}")
            raise

    async def check_for_significant_changes(self, portfolio: dict, threshold: float = 5.0) -> List[str]:
        """Проверка изменений в портфеле за последние 7 дней"""
        notifications = []
        investments = await self.get_investments()
        today = datetime.today().strftime("%d.%m.%Y")
        seven_days_ago = (datetime.today() - timedelta(days=5)).strftime("%d.%m.%Y")

        print(f"Проверка изменений с {seven_days_ago} по {today}")

        for investment_type, data in portfolio.items():
            if investment_type not in investments:
                logger.warning(f"Тип актива {investment_type} не найден в данных инвестиций.")
                continue

            for asset in data:
                asset_name = asset["name"]
                quantity = asset["quantity"]
                price_history = investments[investment_type]

                if seven_days_ago in price_history and today in price_history:
                    old_price_str = price_history[seven_days_ago].get("price", "0")
                    new_price_str = price_history[today].get("price", "0")

                    try:
                        old_price = self.parse_price(old_price_str)
                        new_price = self.parse_price(new_price_str)
                    except ValueError:
                        print(f"Невозможно обработать цены для актива {asset_name}. Пропускаем.")
                        continue

                    price_change = self.get_price_change_percentage(old_price, new_price)

                    if abs(price_change) >= threshold:
                        notifications.append(
                            f"Актив {asset_name} изменил свою цену на {price_change:.2f}% за неделю (текущая цена: {new_price} ₽).")
                        logger.info(f"Уведомление: {asset_name} изменил свою цену на {price_change:.2f}% за неделю.")
                    else:
                        print(f"Изменение цены для {asset_name} менее {threshold}%: {price_change:.2f}%")
                else:
                    logger.warning(f"Нет данных за последние 7 дней для актива {asset_name}.")

                if today in price_history:
                    next_7_day_diff_str = price_history[today].get("next_7_day_diff_in_%", "0")
                    next_7_day_diff = self.parse_percentage(next_7_day_diff_str)
                    if abs(next_7_day_diff) >= threshold:
                        notifications.append(
                            f"Прогноз на актив {asset_name}: изменение цены на {next_7_day_diff:.2f}% за следующие 7 дней.")
                        logger.info(
                            f"Уведомление: прогноз на {asset_name} изменится на {next_7_day_diff:.2f}% за следующие 7 дней.")
                    else:
                        print(
                            f"Прогноз изменения цены для {asset_name} менее {threshold}%: {next_7_day_diff:.2f}%")

        return notifications

    async def check_strategy_end_date(self, end_date: str) -> List[str]:
        """Проверка, если до окончания стратегии осталось менее 7 дней"""
        notifications = []
        today = datetime.today().date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        print(f"Проверка окончания стратегии. Сегодня: {today}, дата окончания: {end_date}")

        if end_date - today <= timedelta(days=7):
            notifications.append("Стратегия заканчивается через 7 дней или меньше. Убедитесь, что вы готовы.")
            logger.info("Стратегия заканчивается через 7 дней или меньше.")
        else:
            print("До окончания стратегии больше 7 дней.")

        return notifications

    async def get_price_by_date_and_name(self, asset_type: str, asset_name: str) -> float:
        investments = await self.get_investments()
        today = date.today().strftime("%d.%m.%Y")

        print(f"Получение цены для актива {asset_name} типа {asset_type} на дату {today}")

        if asset_type not in investments:
            print(f"Неизвестный тип актива: {asset_type}")
            raise ValueError(f"Неизвестный тип актива: {asset_type}")

        asset_data = investments[asset_type]
        if today not in asset_data:
            print(f"Данные по дате {today} не найдены для актива {asset_name}")
            raise ValueError(f"Данные по дате {today} не найдены для актива {asset_name}")

        asset_price_data = asset_data[today]
        if asset_name not in asset_price_data:
            print(f"Цена для актива {asset_name} не найдена на дату {today}")
            raise ValueError(f"Цена для актива {asset_name} не найдена на дату {today}")

        price = asset_price_data[asset_name]["price"]
        price = float(price.replace("₽", "").replace(",", "."))
        print(f"Цена для {asset_name} на {today}: {price} ₽")
        return price
