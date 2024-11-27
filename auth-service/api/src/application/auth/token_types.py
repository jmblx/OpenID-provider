from dataclasses import dataclass
from datetime import datetime
from typing import NewType, TypedDict
from uuid import UUID

from domain.entities.user.value_objects import UserID


class BaseToken(str):
    pass


AccessToken = NewType("AccessToken", BaseToken)
RefreshToken = NewType("RefreshToken", BaseToken)
Fingerprint = NewType("Fingerprint", str)
JTI = str | UUID


class Payload(TypedDict, total=False):
    """Типизированный словарь для представления данных в payload JWT."""

    sub: UserID
    exp: datetime
    iat: datetime
    jti: JTI


class JwtToken(TypedDict):
    token: BaseToken
    expires_in: str
    created_at: str


@dataclass(frozen=True)
class RefreshTokenData:
    token: RefreshToken
    user_id: UserID
    jti: str
    fingerprint: str
    created_at: str
