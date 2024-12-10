import asyncio

import aiohttp
from bs4 import BeautifulSoup

from base_banki_ru_gateway import BaseBankiRuGateway


class SharesGateway(BaseBankiRuGateway):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = "https://www.banki.ru/investment/share/"

    def extract_exchange(self, container: BeautifulSoup) -> str | None:
        exchange_block = container.findAll("div", {"data-test": "investment-security-share-price-diff"})[1]
        exchange = exchange_block.find_next("div", {"class": "OBKaV"}).text.strip() if exchange_block else None
        return exchange

async def main():
    async with aiohttp.ClientSession() as session:
        gateway = SharesGateway(session)
        entity_prices = await gateway.get_entities_prices()
        print(entity_prices)


if __name__ == "__main__":
    asyncio.run(main())
