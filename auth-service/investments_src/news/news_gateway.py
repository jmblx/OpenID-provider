import asyncio

import aiohttp
from bs4 import BeautifulSoup


class NewsGateway:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def _get_news_by_url(self, url: str) -> list[str]:
        async with self.session.get(url) as response:
            html = await response.text()
        soup = BeautifulSoup(html, "lxml")
        container = soup.find("div", class_="rubric-list")
        return [news.text for news in container.find_all("a", class_="list-item__title color-font-hover-only")][:10]


    async def get_politic_news(self) -> dict[str, list[str]]:
        url = "https://ria.ru/location_United_States+location_rossiyskaya-federatsiya+world/"
        return {"politic": await self._get_news_by_url(url)}

    async def get_economic_news(self) -> dict[str, list[str]]:
        url = "https://ria.ru/economy+location_United_States+location_rossiyskaya-federatsiya/"
        return {"economic": await self._get_news_by_url(url)}

    async def get_all_news(self) -> dict[str, list[str]]:
        results = await asyncio.gather(self.get_politic_news(), self.get_economic_news())
        combined_news = {}
        for result in results:
            combined_news.update(result)
        return combined_news
