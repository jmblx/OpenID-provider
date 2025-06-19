import secrets
from abc import ABC, abstractmethod
from typing import TypedDict
from uuid import UUID


class UserRegisterNotifyData(TypedDict):
    email_confirmation_token: str
    email: str


class EmailConfirmationServiceI(ABC):
    @abstractmethod
    async def email_register_notify(
        self, data: UserRegisterNotifyData
    ) -> None:
        pass

    @abstractmethod
    async def save_confirmation_token(
        self, email_confirmation_token: str, user_id
    ) -> None: ...

    @abstractmethod
    async def get_user_id_by_conf_token(
        self, email_confirmation_token: str
    ) -> UUID | None: ...

    @abstractmethod
    async def delete_confirmation_token(
        self, email_confirmation_token: str
    ) -> None: ...

    def generate_email_confirmation_token(self):
        secrets.token_urlsafe(32)
