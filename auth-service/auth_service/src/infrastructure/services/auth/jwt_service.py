from datetime import datetime, timedelta
from typing import cast, Any

import jwt
from pytz import timezone

from application.common.interfaces.jwt_service import JWTService
from application.common.token_types import Payload, JwtToken, BaseToken
from infrastructure.services.auth.config import JWTSettings


class JWTServiceImpl(JWTService):
    """Реализация сервиса работы с JWT токенами."""

    def __init__(self, auth_settings: JWTSettings):
        self.auth_settings = auth_settings

    def encode(
        self,
        payload: Payload,
        expire_minutes: int | None = None,
        expire_timedelta: timedelta | None = None,
    ) -> JwtToken:
        """Создаёт JWT токен с указанным сроком действия."""
        tz = timezone("Europe/Moscow")
        now = datetime.now(tz)

        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(
                minutes=expire_minutes
                or self.auth_settings.access_token_expire_minutes
            )
        payload["exp"] = expire
        payload["iat"] = now
        token = jwt.encode(
            cast(dict[str, Any], payload),
            self.auth_settings.private_key,
            algorithm=self.auth_settings.algorithm,
        )
        return {
            "token": BaseToken(token),
            "created_at": now,
            "expires_at": expire,
        }

    def decode(self, token: BaseToken) -> Payload:
        """Декодирует JWT токен и возвращает его payload."""
        try:
            payload = jwt.decode(
                token,
                self.auth_settings.public_key,
                algorithms=[self.auth_settings.algorithm],
            )
            print(payload, token)
            return cast(Payload, payload)
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.DecodeError:
            raise Exception("Invalid token")
