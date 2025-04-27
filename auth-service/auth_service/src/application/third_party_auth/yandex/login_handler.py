from dataclasses import dataclass

from application.common.interfaces.http_auth import HttpAuthServerService
from application.third_party_auth.common.idp import OAuth2Token
from application.third_party_auth.yandex.idp import YandexIdentityProvider


@dataclass
class YandexLoginCommand:
    yandex_token: OAuth2Token


class YandexLoginHandler:
    def __init__(self, auth_server_service: HttpAuthServerService, yandex_id_provider: YandexIdentityProvider):
        self.auth_server_service = auth_server_service
        self.yandex_id_provider = yandex_id_provider

    async def handle(self, command: YandexLoginCommand):
        user = await self.yandex_id_provider.get_current_user(command.yandex_token)
        tokens = await self.auth_server_service.create_and_save_tokens(user, is_admin=user.is_admin)
        return tokens
