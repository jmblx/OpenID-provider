import asyncio
import aiohttp
from bs4 import BeautifulSoup

from base_banki_ru_gateway import BaseBankiRuGateway


class BondsGateway(BaseBankiRuGateway):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = "https://www.banki.ru/investment/bonds/"

    def extract_exchange(self, container: BeautifulSoup) -> str | None:
        exchange_block = container.find("div", {"data-test": "investment-security-share-price-diff"})
        exchange = exchange_block.find_next("div", {"class": "OBKaV"}).text.strip() if exchange_block else None
        return exchange


async def main():
    async with aiohttp.ClientSession() as session:
        gateway = BondsGateway(session)
        bonds = await gateway.get_entities_prices(tracked_entities=["RU000A1038V6", "RU000A106565", "RU000A108P61", "RU000A104ZK2", "RU000A102KN2"])
        print(bonds)


if __name__ == "__main__":
    asyncio.run(main())
