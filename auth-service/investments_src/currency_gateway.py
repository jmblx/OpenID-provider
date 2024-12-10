from datetime import datetime, timedelta
import pytz
from bs4 import BeautifulSoup
import aiohttp
import asyncio


class CurrenciesGateway:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def get_currencies_for_date(
        self, date: str, currency_codes: list[str]
    ) -> dict:
        """Получить данные валют для конкретной даты."""
        base_url = "https://www.cbr.ru/currency_base/daily/"
        query_params = f"?UniDbQuery.Posted=True&UniDbQuery.To={date}"
        full_url = base_url + query_params

        async with self.session.get(full_url) as response:
            if response.status != 200:
                raise Exception(f"Bad response status: {response.status}")

            text = await response.text()
            soup = BeautifulSoup(text, "lxml")
            table = soup.find("table", class_="data")

            rows = table.find_all("tr")
            currencies = {}

            for row in rows:
                cells = row.find_all("td")
                if cells:
                    code = cells[1].text.strip()
                    if code in currency_codes:
                        units = int(cells[2].text.strip())
                        rate = float(cells[4].text.strip().replace(",", "."))
                        name = cells[3].text.strip()

                        currencies[name] = {
                            "price": round(rate / units, 4),
                            "code": code,
                        }
            return currencies

    async def get_currencies_for_last_days(
        self, days: int, currency_codes: list[str]
    ) -> dict:
        """Получить данные валют за последние N дней."""
        moscow_tz = pytz.timezone("Europe/Moscow")
        current_date = datetime.now(moscow_tz)

        results = {}
        tasks = []

        for i in range(days):
            date = (current_date - timedelta(days=i)).strftime("%d.%m.%Y")
            tasks.append(self.get_currencies_for_date(date, currency_codes))

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for i, response in enumerate(responses):
            date = (current_date - timedelta(days=i)).strftime("%d.%m.%Y")
            if isinstance(response, dict):
                results[date] = response
            else:
                results[date] = {"error": str(response)}

        return results


async def main():
    async with aiohttp.ClientSession() as session:
        gateway = CurrenciesGateway(session)
        needed_codes = ["USD", "AED", "GEL"]
        currencies = await gateway.get_currencies_for_last_days(7, needed_codes)
        print(currencies)
