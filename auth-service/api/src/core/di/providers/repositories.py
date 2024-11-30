from dishka import Provider, Scope, provide

from application.client.interfaces.repo import ClientRepository
from application.user.interfaces.repo import UserRepository
from infrastructure.db.repositories.client_repo_impl import (
    ClientRepositoryImpl,
)
from infrastructure.db.repositories.user_repo_impl import UserRepositoryImpl


class RepositoriesProvider(Provider):
    user_repo = provide(
        UserRepositoryImpl, scope=Scope.REQUEST, provides=UserRepository
    )
    client_repo = provide(
        ClientRepositoryImpl, scope=Scope.REQUEST, provides=ClientRepository
    )
