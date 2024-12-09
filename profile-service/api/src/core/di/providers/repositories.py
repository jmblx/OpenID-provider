from dishka import Provider, Scope, provide

from application.role.interfaces.repo import RoleRepository
from application.user.interfaces.repo import UserRepository
from infrastructure.db.repositories.role_repository import RoleRepositoryImpl
from infrastructure.db.repositories.user_repo_impl import UserRepositoryImpl


class RepositoriesProvider(Provider):
    user_repo = provide(
        UserRepositoryImpl, scope=Scope.REQUEST, provides=UserRepository
    )
    role_repo = provide(
        RoleRepositoryImpl, scope=Scope.REQUEST, provides=RoleRepository
    )
