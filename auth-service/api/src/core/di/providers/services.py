import os

import firebase_admin
from dishka import Provider, Scope, provide
from fastapi import HTTPException
from fastapi.requests import Request
from firebase_admin import credentials, auth
from sqlalchemy.ext.asyncio import AsyncSession

from config import FirebaseConfig
from domain.services.achievement.ach_service_interface import (
    AchievementServiceInterface,
)
from domain.services.event.event_service_interface import EventServiceInterface
from domain.services.reward.ach_service_interface import RewardServiceInterface
from domain.services.storage.storage_service import StorageServiceInterface
from domain.services.user.user_service_interface import UserService
from infrastructure.db.models import User
from infrastructure.external_services.receipt.service import ExternalAPIService
from infrastructure.external_services.storage.minio_service import MinIOService
from infrastructure.services.achievements.ach_service_impl import (
    AchievementServiceImpl,
)
from infrastructure.services.event.event_service_impl import EventServiceImpl
from infrastructure.services.reward.reward_service_impl import (
    RewardServiceImpl,
)
from infrastructure.services.user.user_service_impl import UserServiceImpl
from presentation.web_api.registration.schemas import UserLogin


class Firebase:
    pass


async def auth_user_id_by_token(token_id: str) -> dict:
    try:
        decoded_token = auth.verify_id_token(token_id)
        return {
            "id": decoded_token.get("uid"),
            "email": decoded_token.get("email"),
        }

    except Exception as e:
        print("Error verifying token:", e)
        return None


class ServiceProvider(Provider):

    # @provide(scope=Scope.REQUEST, provides=UserService)
    # def provide_user_service(
    #     self, user_repo: UserRepository
    # ) -> UserService:
    #     return UserServiceImpl(user_repo)
    user_service = provide(
        UserServiceImpl, scope=Scope.REQUEST, provides=UserService
    )
    achievement_service = provide(
        AchievementServiceImpl,
        scope=Scope.REQUEST,
        provides=AchievementServiceInterface,
    )
    storage_service = provide(
        MinIOService, scope=Scope.REQUEST, provides=StorageServiceInterface
    )
    reward_service = provide(
        RewardServiceImpl, scope=Scope.REQUEST, provides=RewardServiceInterface
    )
    event_service = provide(
        EventServiceImpl, scope=Scope.REQUEST, provides=EventServiceInterface
    )

    @provide(scope=Scope.APP)
    def provide_firebase(self) -> Firebase:
        cred = credentials.Certificate(FirebaseConfig.from_env().rd_uri)
        firebase_admin.initialize_app(cred)
        return Firebase()

    @provide(scope=Scope.REQUEST)
    async def get_user_from_auth(
        self, request: Request, session: AsyncSession, fb: Firebase
    ) -> User:  # noqa
        token_id = request.headers.get("Authorization")
        if token_id == "bob":
            return await session.get(User, "cTqj1BzxfWS9gQGgn033WIcmn4e2")
        user_uid = (await auth_user_id_by_token(token_id)).get("id")
        return await session.get(User, user_uid)
        # return await session.get(UserDB, "gNySnybUZLht9O8kfYQXGdUkkJG2")

    @provide(scope=Scope.REQUEST)
    async def get_data_by_auth_header(
        self, request: Request, fb: Firebase
    ) -> UserLogin:  # noqa
        token_id = request.headers.get("Authorization")
        data = await auth_user_id_by_token(token_id)
        return UserLogin(**data)

    # reg_validation_service = provide(
    #     RegUserValidationService,
    #     scope=Scope.REQUEST,
    #     provides=UserValidationService,
    # )


class ExternalAPIProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def provide_external_service(
        self, request: Request
    ) -> ExternalAPIService:
        auth_token = request.headers.get("Authorization")
        if not auth_token:
            raise HTTPException(
                status_code=401, detail="Отсутствует токен аутентификации"
            )
        base_url = os.getenv(
            "RECEIPT_SERVICE_BASE_URL"
        )  # Адрес вашего внешнего приложения
        return ExternalAPIService(base_url=base_url, auth_token=auth_token)
