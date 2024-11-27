from typing import Any

from infrastructure.db.models import User
from domain.services.auth.auth_service import AuthService
from domain.services.user.access_policy import UserAccessPolicyInterface
from domain.services.user.user_service_interface import UserService
import logging


class DeleteAndReadUserUseCase:
    def __init__(
        self,
        user_service: UserService,
        access_policy: UserAccessPolicyInterface,
        auth_service: AuthService,
    ):
        self.user_service = user_service
        self.access_policy = access_policy
        self.auth_service = auth_service

    async def __call__(
        self,
        auth_token: str,
        search_data: dict[Any, Any],
        selected_fields: dict[Any, dict[Any, dict]],
        order_by: dict,
        full_delete: bool,
    ) -> list[User] | User:
        required_data_requester, required_data_user, checks = (
            await self.access_policy.get_required_data("delete", search_data)
        )

        requester = await self.auth_service.get_user_by_token(
            auth_token, required_data_requester.get("user")
        )

        target_users = await self.user_service.get_many_by_fields(
            search_data, required_data_user
        )
        for target_user in target_users:
            target_user_data = {"user": {"id": target_user.id}}
            if not await self.access_policy.check_access(
                requester, required_data_requester, target_user_data, checks
            ):
                logging.warning(
                    f"Access denied for user {requester.id} to delete user {target_user.id}"
                )
                raise PermissionError(
                    f"Access denied to delete user {target_user.id}"
                )
        users = await self.user_service.delete_and_fetch(
            search_data, selected_fields, order_by, full_delete
        )

        return users


class DeleteUserUseCase:
    def __init__(
        self,
        user_service: UserService,
        access_policy: UserAccessPolicyInterface,
        auth_service: AuthService,
    ):
        self.user_service = user_service
        self.access_policy = access_policy
        self.auth_service = auth_service

    async def __call__(
        self,
        auth_token: str,
        search_data: dict[Any, Any],
        full_delete: bool,
    ) -> None:
        required_data_requester, required_data_user, checks = (
            await self.access_policy.get_required_data("delete")
        )

        requester = await self.auth_service.get_user_by_token(
            auth_token, required_data_requester.get("user")
        )

        target_users = await self.user_service.get_many_by_fields(
            search_data, required_data_user
        )
        logging.info(
            f"required_data_user: {required_data_user, required_data_requester, checks}"
        )
        for target_user in target_users:
            target_user_data = {"user": {"id": target_user.id}}
            if not await self.access_policy.check_access(
                requester, required_data_requester, target_user_data, checks
            ):
                logging.warning(
                    f"Access denied for user {requester.id} to delete user {target_user.id}"
                )
                raise PermissionError(
                    f"Access denied to delete user {target_user.id}"
                )

        await self.user_service.delete_by_fields(search_data, full_delete)
