import aiohttp
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.third_party_auth.common.idp import OauthIdentityProvider, OAuth2Token
from domain.entities.user.model import User
from domain.entities.user.value_objects import Email


class YandexIdentityProvider(OauthIdentityProvider):
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_yandex_user_email(self, oauth_token: str) -> str:
        if not oauth_token:
            raise ValueError("Токен не может быть пустым")

        headers = {"Authorization": f"OAuth {oauth_token}"}
        url = "https://login.yandex.ru/info?format=json"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return data.get("default_email")

        except aiohttp.ClientResponseError as e:
            raise ValueError(f"Ошибка запроса к Яндекс ID: {e.status} - {e.message}")
        except aiohttp.ClientError as e:
            raise ValueError(f"Сетевая ошибка: {str(e)}")
        except (KeyError, ValueError) as e:
            raise ValueError(f"Ошибка обработки ответа: {str(e)}")

    async def get_current_user(self, oauth_token: str) -> User:
        email = await self.get_yandex_user_email(oauth_token)
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise ValueError("Пользователь с таким email не найден")
        return user
