from dishka import Provider, provide, Scope

from application.client.interfaces.reader import ClientReader
from application.user.interfaces.reader import UserReader
from infrastructure.db.readers.client_reader import ClientReaderImpl
from infrastructure.db.readers.user_reader import UserReaderImpl


class ReaderProvider(Provider):
    user_reader = provide(
        UserReaderImpl, scope=Scope.REQUEST, provides=UserReader
    )
    client_reader = provide(
        ClientReaderImpl, scope=Scope.REQUEST, provides=ClientReader
    )
