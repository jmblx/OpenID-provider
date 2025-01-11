import logging
from uuid import UUID

import redis.asyncio as aioredis
from nats.aio.client import Client

from application.common.interfaces.email_confirmation_service import (
    EmailConfirmationServiceI,
)
from infrastructure.external_services.message_routing.config import NatsConfig
from infrastructure.external_services.message_routing.nats_utils import (
    send_via_nats,
)


logger = logging.getLogger(__name__)


class EmailConfirmationService(EmailConfirmationServiceI):
    def __init__(
        self,
        redis: aioredis.Redis,
        nats_client: Client,
        nats_config: NatsConfig,
    ):
        self._nats_client = nats_client
        self._nats_config = nats_config
        self._redis = redis

    async def email_register_notify(self, data: dict) -> None:
        logger.info(
            "email_register_notify: data: %s  sub: %s",
            data,
            self._nats_config.email_confirmation_sub,
        )
        await send_via_nats(
            self._nats_client,
            self._nats_config.email_confirmation_sub,
            data=data,
        )

    async def save_confirmation_token(
        self, email_confirmation_token: str, user_id: UUID
    ) -> None:
        await self._redis.set(
            f"email_confirmation_token:{email_confirmation_token}",
            user_id.hex,
            ex=1800,
        )

    async def get_user_id_by_conf_token(
        self, email_confirmation_token: str
    ) -> UUID | None:
        user_id = await self._redis.get(
            f"email_confirmation_token:{email_confirmation_token}"
        )
        if user_id is None:
            return None
        return UUID(user_id)

    async def delete_confirmation_token(
        self, email_confirmation_token: str
    ) -> None:
        await self._redis.delete(
            f"email_confirmation_token:{email_confirmation_token}"
        )
