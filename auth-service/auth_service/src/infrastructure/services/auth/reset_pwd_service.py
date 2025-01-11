from datetime import timedelta
from uuid import UUID

from redis.asyncio import Redis

from application.user.reset_pwd.service import (
    ResetPwdService,
    ResetPasswordToken,
)


class ResetPwdServiceImpl(ResetPwdService):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def save_password_reset_token(
        self, user_id: UUID, token: ResetPasswordToken
    ) -> None:
        await self.redis.set(
            f"reset_password:{token}", str(user_id), ex=timedelta(minutes=15)
        )

    async def get_user_id_from_reset_pwd_token(
        self, token: ResetPasswordToken
    ) -> UUID | None:
        user_id = await self.redis.get(f"reset_password:{token}")
        return UUID(user_id) if user_id else None

    async def delete_reset_pwd_token(self, token: ResetPasswordToken) -> None:
        await self.redis.delete(f"reset_password:{token}")
