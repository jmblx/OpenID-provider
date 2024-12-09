from dishka import Provider, provide, Scope

from application.user.interfaces.reader import UserReader
from infrastructure.db.readers.user_reader import UserReaderImpl


class ReaderProvider(Provider):
    user_reader = provide(UserReaderImpl, scope=Scope.REQUEST, provides=UserReader)
