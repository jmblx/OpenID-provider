from abc import ABC, abstractmethod
from typing import NewType
from uuid import UUID


ResetPasswordToken = NewType("ResetPasswordToken", str)


class ResetPwdService(ABC):
    @abstractmethod
    async def save_password_reset_token(
        self, user_id: UUID, token: ResetPasswordToken
    ) -> None: ...

    @abstractmethod
    async def get_user_id_from_reset_pwd_token(
        self, token: ResetPasswordToken
    ) -> UUID | None: ...

    @abstractmethod
    async def delete_reset_pwd_token(
        self, token: ResetPasswordToken
    ) -> None: ...
