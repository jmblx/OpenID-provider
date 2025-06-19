from dishka import Provider, Scope, provide

from application.client.common.client_reader import ClientReader
from application.common.interfaces.user_reader import UserReader
from application.resource_server.common.rs_reader import ResourceServerReader
from infrastructure.db.readers.client_reader import ClientReaderImpl
from infrastructure.db.readers.rs_reader import ResourceServerReaderImpl
from infrastructure.db.readers.user_reader import UserReaderImpl


class ReaderProvider(Provider):
    user_reader = provide(
        UserReaderImpl, scope=Scope.REQUEST, provides=UserReader
    )
    client_reader = provide(
        ClientReaderImpl, scope=Scope.REQUEST, provides=ClientReader
    )
    resource_server_reader = provide(
        ResourceServerReaderImpl,
        scope=Scope.REQUEST,
        provides=ResourceServerReader,
    )
    # strategy_reader = provide(StrategyReader, scope=Scope.REQUEST)
