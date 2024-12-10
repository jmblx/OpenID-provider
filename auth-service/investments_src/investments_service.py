import json

import redis.asyncio as aioredis

from bonds_gateway import BondsGateway
from currency_gateway import CurrenciesGateway
from gold_gateway import GoldGateway
from share_gateway import SharesGateway


class InvestmentsService:
    def __init__(self, bonds_gate: BondsGateway, currency_gate: CurrenciesGateway, gold_gate: GoldGateway, share_gate: SharesGateway, redis: aioredis.Redis):
        self.bonds_gateway = bonds_gate
        self.currency_gateway = currency_gate
        self.gold_gateway = gold_gate
        self.share_gateway = share_gate
        self.redis = redis

    async def get_existing_data_from_redis(self, key):
        data = await self.redis.get(key)
        if data:
            return json.loads(data)
        return {}

    async def get_all_data(self):
        bonds = await self.bonds_gateway.get_entities_prices(
            tracked_entities=["RU000A1038V6", "RU000A106565", "RU000A108P61", "RU000A104ZK2", "RU000A102KN2"]
        )
        currencies = await self.currency_gateway.get_currencies_for_last_days(7, ["USD", "AED", "GEL"])
        gold = await self.gold_gateway.get_gold_prices(7)
        shares = await self.share_gateway.get_entities_prices(
            tracked_entities=["aeroflot_AFLT", "detskiymir_DSKY", "lenta_LENT", "sberbankp_SBERP", "RussNeft_RNFT"]
        )

        existing_bonds = await self.get_existing_data_from_redis("bonds")
        existing_shares = await self.get_existing_data_from_redis("shares")

        all_data = {
            "bonds": self.merge_data(existing_bonds, bonds),
            "currencies": currencies,
            "gold": gold,
            "shares": self.merge_data(existing_shares, shares)
        }

        await self.redis.set("data", json.dumps(all_data))

    def merge_data(self, existing_data, new_data):
        all_dates = list({**existing_data, **new_data}.keys())[-7:]
        merged_data = {}
        for date in all_dates:
            if date in new_data:
                merged_data[date] = new_data[date]
            elif date in existing_data:
                merged_data[date] = existing_data[date]

        return merged_data
