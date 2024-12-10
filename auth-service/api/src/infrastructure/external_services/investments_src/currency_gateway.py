import aiohttp
from bs4 import BeautifulSoup


class CurrencyGateway:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def get_5_currencies(self):
        async with self.session.get("https://www.sravni.ru/valjuty/cb-rf/usd/") as response:
            if response.status != 200:
                raise Exception(f"Bad response status: {response.status}")
            text = await response.text()
            soup = BeautifulSoup(text, "lxml")
            print(soup.get())
