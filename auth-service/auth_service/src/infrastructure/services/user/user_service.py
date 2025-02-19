from application.common.interfaces.role_repo import RoleRepository
from application.common.interfaces.user_repo import UserRepository
from application.user.user_service import UserService
from domain.entities.client.model import Client
from domain.entities.user.model import User


class UserServiceImpl(UserService):
    def __init__(
        self, user_repository: UserRepository, role_repository: RoleRepository
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository

    async def add_client_to_user(self, user: User, client: Client):
        user.clients.append(client)
        await self.user_repository.save(user)
        new_roles = await self.role_repository.get_base_client_roles(
            client_id=client.id
        )
        await self.user_repository.add_roles_to_user(
            user.id, [role.id for role in new_roles]
        )
