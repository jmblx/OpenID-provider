from abc import ABC, abstractmethod
from application.common.token_types import (
    Fingerprint,
    AccessToken,
    RefreshToken,
)
from domain.entities.user.model import User
from domain.entities.user.value_objects import Email, RawPassword


class HttpAuthService(ABC):
    """Абстракция для сервиса аутентификации и управления токенами."""

    @abstractmethod
    async def revoke(self, refresh_token: RefreshToken) -> None:
        """
        Инвалидация RefreshToken (logout пользователя).

        :param refresh_token: Токен, который необходимо аннулировать.
        """

    @abstractmethod
    async def invalidate_other_tokens(
        self, refresh_token: RefreshToken, fingerprint: Fingerprint
    ) -> None:
        """
        Инвалидирует все токены пользователя, кроме текущего.
        """

    # @abstractmethod
    # async def authenticate_by_auth_code(
    #     self,
    #     auth_code: str,
    #     redirect_url: str,
    #     fingerprint: Fingerprint,
    #     code_challenger: str,
    #     user_scopes: list[str],
    # ) -> tuple[AccessToken, RefreshToken]:
    #     """
    #     Аутентифицирует пользователя с использованием авторизационного кода.
    #
    #     :param auth_code: Авторизационный код.
    #     :param redirect_url: URL для редиректа после авторизации.
    #     :param fingerprint: Отпечаток устройства пользователя.
    #     :param code_challenger: Код подтверждения для PKCE.
    #     :return: Пара AccessToken и RefreshToken.
    #     """

    @abstractmethod
    async def create_and_save_tokens(
        self,
        user: User,
        fingerprint: Fingerprint,
        user_scopes: list[str],
        client_id: int,
    ) -> tuple[AccessToken, RefreshToken]: ...

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
