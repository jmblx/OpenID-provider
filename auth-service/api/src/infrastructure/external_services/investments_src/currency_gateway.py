import asyncio
from datetime import datetime

import aiohttp
import pytz
from bs4 import BeautifulSoup


class CurrencyGateway:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def get_currencies(self):
        moscow_tz = pytz.timezone('Europe/Moscow')
        current_date = datetime.now(moscow_tz).strftime('%d.%m.%Y')
        base_url = "https://www.cbr.ru/currency_base/daily/"
        query_params = f"?UniDbQuery.Posted=True&UniDbQuery.To={current_date}"
        full_url = base_url + query_params
        async with self.session.get(full_url) as response:
            if response.status != 200:
                raise Exception(f"Bad response status: {response.status}")
            text = await response.text()
            soup = BeautifulSoup(text, "lxml")
            table = soup.find('table', class_='data')

            rows = table.find_all('tr')

            usd_data = {}
            for row in rows:
                cells = row.find_all('td')
                if cells and cells[1].text.strip() == 'USD':
                    usd_data['Цифр. код'] = cells[0].text.strip()
                    usd_data['Букв. код'] = cells[1].text.strip()
                    usd_data['Единиц'] = cells[2].text.strip()
                    usd_data['Валюта'] = cells[3].text.strip()
                    usd_data['Курс'] = cells[4].text.strip()

            print(usd_data)

async def main():
    async with aiohttp.ClientSession() as session:
        gateway = CurrencyGateway(session)
        await gateway.get_5_currencies()

asyncio.run(main())
