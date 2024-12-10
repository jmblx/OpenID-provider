import json
import redis.asyncio as aioredis
import logging

from bonds_gateway import BondsGateway
from currency_gateway import CurrenciesGateway
from gold_gateway import GoldGateway
from deposit_gateway import DepositGateway
from news.news_gateway import NewsGateway
from predict.gateway import PredictionGateway
from share_gateway import SharesGateway


class InvestmentsService:
    def __init__(
            self,
            bonds_gate: BondsGateway,
            currency_gate: CurrenciesGateway,
            gold_gate: GoldGateway,
            share_gate: SharesGateway,
            deposit_gateway: DepositGateway,
            news_gateway: NewsGateway,
            prediction_gateway: PredictionGateway,
            redis: aioredis.Redis,
    ):
        self.bonds_gateway = bonds_gate
        self.currency_gateway = currency_gate
        self.gold_gateway = gold_gate
        self.share_gateway = share_gate
        self.deposit_gateway = deposit_gateway
        self.news_gateway = news_gateway
        self.redis = redis
        self.prediction_gateway = prediction_gateway
        self.logger = logging.getLogger(__name__)

    async def get_existing_data_from_redis(self, key):
        self.logger.info(f"Fetching existing data from Redis for key: {key}")
        data = await self.redis.get(key)
        if data:
            return json.loads(data)
        return {}

    async def collect_all_data(self):
        # Собираем текущие данные
        bonds = await self.bonds_gateway.get_entities_prices(
            tracked_entities=[
                "RU000A1038V6",
                "RU000A106565",
                "RU000A108P61",
                "RU000A104ZK2",
                "RU000A102KN2",
            ]
        )

        currencies = await self.currency_gateway.get_currencies_for_last_days(
            7, ["USD", "AED", "GEL"]
        )

        gold = await self.gold_gateway.get_gold_prices(7)

        shares = await self.share_gateway.get_entities_prices(
            tracked_entities=[
                "aeroflot_AFLT",
                "detskiymir_DSKY",
                "lenta_LENT",
                "sberbankp_SBERP",
                "RussNeft_RNFT",
            ]
        )

        deposits = self.deposit_gateway.get_deposits()

        existing_bonds = await self.get_existing_data_from_redis("bonds")
        existing_currencies = await self.get_existing_data_from_redis("currencies")
        existing_gold = await self.get_existing_data_from_redis("gold")
        existing_shares = await self.get_existing_data_from_redis("shares")

        news_data = await self.news_gateway.get_all_news()

        historical_data = {
            "bonds": existing_bonds,
            "currencies": existing_currencies,
            "gold": existing_gold,
            "shares": existing_shares,
        }

        self.logger.info("Requesting predictions based on news and historical data")
        predictions = self.prediction_gateway.get_predictions(news_data, historical_data)

        self.logger.info("Merging and calculating all data")
        all_data = {
            "bonds": self.merge_and_calculate(existing_bonds, bonds, predictions.get("bonds", {})),
            "currencies": self.merge_and_calculate(existing_currencies, currencies, predictions.get("currencies", {})),
            "gold": self.merge_and_calculate(existing_gold, gold, predictions.get("gold", {})),
            "shares": self.merge_and_calculate(existing_shares, shares, predictions.get("shares", {})),
            "deposits": deposits,
        }

        self.logger.info("Saving merged data to Redis")
        await self.redis.set("data", json.dumps(all_data))

    def merge_and_calculate(self, existing_data, new_data, predicted_data):
        self.logger.info("Merging data from existing, new, and predictions")
        all_dates = list({**existing_data, **new_data, **predicted_data}.keys())[-7:]
        merged_data = {}

        for date in all_dates:
            if date in new_data:
                merged_data[date] = new_data[date]
            elif date in existing_data:
                merged_data[date] = existing_data[date]
            elif date in predicted_data:
                merged_data[date] = predicted_data[date]

        if merged_data:
            first_date, last_date = all_dates[0], all_dates[-1]
            for entity, details in merged_data[last_date].items():
                self.logger.info(f"Calculating changes for {entity}")
                first_price = self.extract_price(merged_data[first_date].get(entity, {}).get("price"))
                last_price = self.extract_price(details.get("price"))

                if first_price is not None and last_price is not None:
                    percentage_change = self.calculate_percentage_change(first_price, last_price)
                    details["percentage_change"] = f"{percentage_change:.2f}%"
                else:
                    details["percentage_change"] = "0.00%"

                # Add predicted change if available
                if "predicted_price" in details:
                    predicted_price = self.extract_price(details["predicted_price"])
                    if predicted_price is not None and last_price is not None:
                        predicted_change = self.calculate_percentage_change(last_price, predicted_price)
                        details["predicted_change"] = f"{predicted_change:.2f}%"
                    else:
                        details["predicted_change"] = "0.00%"

        return merged_data

    @staticmethod
    def extract_price(price):
        if price is None:
            return None
        try:
            return float(price.replace("\u20bd", "").replace(",", ""))
        except ValueError:
            return None

    @staticmethod
    def calculate_percentage_change(first_price, last_price):
        if first_price == 0:
            return 0
        return ((last_price - first_price) / first_price) * 100