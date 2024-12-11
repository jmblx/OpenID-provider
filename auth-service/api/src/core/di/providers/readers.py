from dishka import Provider, provide, Scope

from application.user.interfaces.reader import UserReader
from infrastructure.db.readers.client_reader import ClientReaderImpl
from infrastructure.db.readers.strategy_reader import StrategyReader
from infrastructure.db.readers.user_reader import UserReaderImpl
from application.client.reader import ClientReader


class ReaderProvider(Provider):
    user_reader = provide(UserReaderImpl, scope=Scope.REQUEST, provides=UserReader)
    client_reader = provide(
        ClientReaderImpl, scope=Scope.REQUEST, provides=ClientReader
    )
    strategy_reader = provide(StrategyReader, scope=Scope.REQUEST)
