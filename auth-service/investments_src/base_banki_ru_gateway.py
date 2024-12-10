import asyncio
from abc import abstractmethod
from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup


class BaseBankiRuGateway:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0"
        }

    async def get_entities_prices(
        self, tracked_entities: list[str] = None
    ) -> dict[str, dict]:
        tasks = [self.parse_current_entity(entity) for entity in tracked_entities]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        today_date = datetime.now().strftime("%d.%m.%Y")
        aggregated_data = {today_date: {}}

        for entity, result in zip(tracked_entities, results):
            if isinstance(result, dict):
                aggregated_data[today_date].update(result)
            else:
                aggregated_data[today_date][entity] = {"error": str(result)}

        return aggregated_data

    async def parse_current_entity(self, entity: str, retries=3) -> dict:
        url = f"{self.base_url}{entity}"
        for attempt in range(retries):
            try:
                async with self.session.get(
                    url, headers=self.headers, allow_redirects=True
                ) as response:
                    if response.status != 200:
                        raise Exception(f"Bad response status: {response.status}")

                    html = await response.text()
                    return self.extract_entity_data(html)

            except Exception as e:
                print(f"Error fetching {url} on attempt {attempt + 1}/{retries}: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(1)

        return {"error": "Failed to fetch data after retries"}

    @abstractmethod
    def extract_exchange(self, soup: BeautifulSoup) -> str | None: ...

    def extract_entity_data(self, html: str) -> dict:
        soup = BeautifulSoup(html, "lxml")

        try:
            container = soup.find("div", class_="GridVertical__sc-1qp5ykd-0 bTOBbO")
            name = container.find("h1", {"data-test": "investment-security-title"})
            name = name.text.replace("купить онлайн", "").strip() if name else "Unknown"

            price = container.find(
                "div", {"data-test": "investment-item-price-block__price"}
            )
            price = price.text.strip() if price else None

            sector = container.find("div", {"class": "OBKaV"}).text.strip()

            country = soup.find(
                "div", {"data-test": "investment-security-issuer-sector"}
            )
            country = country.find_next_sibling("div").text.strip() if country else None

            exchange = self.extract_exchange(soup)

            return {
                name: {
                    "price": price,
                    "sector": sector,
                    "country": country.replace("Страна: ", "") if country else None,
                    "exchange": exchange,
                }
            }

        except Exception as e:
            return {"error": str(e)}
