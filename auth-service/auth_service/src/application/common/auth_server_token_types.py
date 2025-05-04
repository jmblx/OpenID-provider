from dataclasses import dataclass
from datetime import datetime, timedelta
from statistics import covariance
from typing import NewType, TypedDict
from uuid import UUID

from domain.entities.user.value_objects import UserID


class BaseToken(str):
    pass


AccessToken = NewType("AccessToken", BaseToken)
RefreshToken = NewType("RefreshToken", BaseToken)
Fingerprint = NewType("Fingerprint", str)

class AuthServerAccessTokenPayload(TypedDict, total=False):
    """Типизированный словарь для представления данных в payload JWT."""
    sub: UserID
    exp: datetime
    iat: datetime
    jti: UUID


class AccessTokenPayload(TypedDict):
    sub: str
    email: str
    scopes: dict[str, str]


class JwtToken(TypedDict):
    token: BaseToken
    created_at: datetime
    expires_at: datetime


@dataclass
class AuthServerRefreshTokenData:
    user_id: UUID
    jti: str
    fingerprint: Fingerprint | None
    created_at: datetime

class RefreshTokenPayload(TypedDict):
    sub: str
    jti: UUID


@dataclass
class AuthServerRefreshTokenWithData(AuthServerRefreshTokenData):
    token: RefreshToken
