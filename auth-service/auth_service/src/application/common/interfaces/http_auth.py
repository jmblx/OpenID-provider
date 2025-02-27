from abc import ABC, abstractmethod
from uuid import UUID

from application.auth_as.common.types import (
    AuthServerAccessToken,
    AuthServerRefreshToken,
    AuthServerTokens,
)
from application.common.auth_server_token_types import (
    Fingerprint,
    AccessToken,
    RefreshToken,
)
from application.common.client_token_types import ClientTokens
from domain.entities.user.model import User
from domain.entities.user.value_objects import Email, RawPassword


class HttpService(ABC):
    @abstractmethod
    async def invalidate_other_tokens(
        self, refresh_token: RefreshToken, fingerprint: Fingerprint
    ) -> None:
        """
        Инвалидирует все токены пользователя, кроме текущего.
        """

    @abstractmethod
    async def revoke(self, refresh_token: RefreshToken) -> None:
        """
        Инвалидация RefreshToken (logout пользователя).

        :param refresh_token: Токен, который необходимо аннулировать.
        """

    # @abstractmethod
    # async def invalidate_user_tokens(
    #         self, user: User
    # ) -> None:
    #     """
    #     Инвалидирует все активные токены пользователя.
    #
    #     Используется, например, при сбросе пароля или принудительном выходе.
    #     :param user: Экземпляр пользователя.
    #     """

    # @abstractmethod
    # async def list_active_tokens(
    #         self, user: User
    # ) -> list[dict]:
    #     """
    #     Возвращает список активных токенов пользователя.
    #
    #     Может использоваться для управления сессиями.
    #     :param user: Экземпляр пользователя.
    #     :return: Список активных токенов с метаданными.
    #     """


class HttpAuthServerService(HttpService):
    """Абстракция для сервиса аутентификации и управления токенами."""
    @abstractmethod
    async def create_and_save_tokens(
        self,
        user: User,
        fingerprint: Fingerprint | None = None,
    ) -> AuthServerTokens: ...


class HttpClientService(HttpService):
    @abstractmethod
    async def create_and_save_tokens(
        self,
        user: User,
        user_scopes: list[str],
        client_id: int,
        fingerprint: Fingerprint | None = None,
    ) -> ClientTokens: ...
