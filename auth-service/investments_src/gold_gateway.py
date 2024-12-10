from datetime import datetime, timedelta
import pytz
from bs4 import BeautifulSoup
import aiohttp


class GoldGateway:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def get_gold_prices(self, days: int) -> dict:
        """Получить данные о цене на золото за последние N дней."""
        moscow_tz = pytz.timezone("Europe/Moscow")
        end_date = datetime.now(moscow_tz).strftime("%d.%m.%Y")
        start_date = (datetime.now(moscow_tz) - timedelta(days=days - 1)).strftime(
            "%d.%m.%Y"
        )

        base_url = "https://www.cbr.ru/hd_base/metall/metall_base_new/"
        query_params = (
            f"?UniDbQuery.Posted=True&UniDbQuery.From={start_date}&UniDbQuery.To={end_date}"
            f"&UniDbQuery.Gold=true&UniDbQuery.so=0"
        )
        full_url = base_url + query_params

        async with self.session.get(full_url) as response:
            if response.status != 200:
                raise Exception(f"Bad response status: {response.status}")

            text = await response.text()
            soup = BeautifulSoup(text, "lxml")
            table = soup.find("table", class_="data")

            rows = table.find_all("tr")[1:]
            gold_prices = {}

            for row in rows:
                cells = row.find_all("td")
                if cells:
                    date = cells[0].text.strip()
                    price = float(
                        cells[1].text.strip().replace(" ", "").replace(",", ".")
                    )
                    gold_prices[date] = {"price": price}

            all_dates = [
                (datetime.now(moscow_tz) - timedelta(days=i)).strftime("%d.%m.%Y")
                for i in range(days)
            ]

            last_known_price = None
            filled_prices = {}
            for date in reversed(all_dates):
                if date in gold_prices:
                    last_known_price = gold_prices[date]["price"]
                filled_prices[date] = {"price": last_known_price}

            return filled_prices


async def main():
    async with aiohttp.ClientSession() as session:
        gateway = GoldGateway(session)
        gold_prices = await gateway.get_gold_prices(7)
        print(gold_prices)
