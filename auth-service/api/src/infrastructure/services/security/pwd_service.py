from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from domain.services.security.pwd_service import HashService


class HashServiceImpl(HashService):
    def __init__(self):
        self.ph = PasswordHasher()

    def hash_password(self, password: str) -> bytes:
        hashed_password_str = self.ph.hash(password)
        return hashed_password_str.encode("utf-8")

    def check_password(
        self, plain_password: str, hashed_password: bytes
    ) -> bool:
        try:
            hashed_password_str = hashed_password.decode("utf-8")
            self.ph.verify(hashed_password_str, plain_password)
            return True
        except VerifyMismatchError:
            return False
