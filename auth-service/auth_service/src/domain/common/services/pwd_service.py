from abc import ABC, abstractmethod

from domain.entities.user.value_objects import RawPassword, HashedPassword


class PasswordHasher(ABC):

    @abstractmethod
    def hash_password(self, raw_password: RawPassword) -> HashedPassword:
        pass

    @abstractmethod
    def check_password(
        self, plain_password: RawPassword, hashed_password: HashedPassword
    ) -> None:
        pass
