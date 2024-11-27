import secrets
from typing import Any

from domain.services.security.pwd_service import HashService
from domain.services.user.user_service_interface import UserService
from domain.services.user.validation import UserValidationService
from infrastructure.external_services.message_routing.notify_service import (
    NotifyService,
)


class CreateUserUseCase:
    def __init__(
        self,
        user_service: UserService,
        validation_service: UserValidationService,
    ):
        self.user_service = user_service
        self.validation_service = validation_service

    async def __call__(
        self,
        user_data: dict,
        selected_fields: dict[Any, dict[Any, dict]],
    ):
        self.validation_service.validate_create_data(user_data)
        user_id = await self.user_service.register(user_data, selected_fields)

        return user_id
