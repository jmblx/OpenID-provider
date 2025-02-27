import logging
from datetime import timedelta
from uuid import UUID, uuid4

from application.common.auth_server_token_types import AccessToken, Fingerprint
from application.common.client_token_types import ClientRefreshTokenWithData, ClientAccessToken
from application.common.interfaces.client_token_creation import ClientTokenCreationService
from application.common.interfaces.jwt_service import JWTService
from infrastructure.services.auth.config import JWTSettings


logger = logging.getLogger(__name__)


class ClientTokenCreationServiceImpl(ClientTokenCreationService):
    def __init__(self, jwt_settings: JWTSettings, jwt_service: JWTService):
        self.jwt_service = jwt_service
        self.jwt_settings = jwt_settings

    def create_client_access_token(
        self, user_id: UUID, user_scopes: list[str]
    ) -> ClientAccessToken:
        logger.info("scopes: %s", user_scopes)
        jwt_payload = {
            "sub": str(user_id),
            "jti": uuid4().hex,
            "scopes": user_scopes,
        }
        encoded_token = self.jwt_service.encode(
            payload=jwt_payload,
            expire_minutes=self.jwt_settings.access_token_expire_minutes,
        )
        return ClientAccessToken(encoded_token["token"])

    async def create_client_refresh_token(
        self, user_id: UUID, fingerprint: Fingerprint, client_id: int,
    ) -> ClientRefreshTokenWithData:
        jti = uuid4().hex
        jwt_payload = {"sub": user_id.hex, "jti": jti, "client_id": client_id}
        encoded_token = self.jwt_service.encode(
            payload=jwt_payload,
            expire_timedelta=timedelta(
                days=self.jwt_settings.refresh_token_expire_days
            ),
        )
        refresh_token_data = ClientRefreshTokenWithData(
            token=encoded_token["token"],  # type: ignore
            user_id=user_id,
            jti=jti,
            fingerprint=fingerprint,
            created_at=encoded_token["created_at"],
        )
        return refresh_token_data
