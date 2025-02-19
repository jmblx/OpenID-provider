from dataclasses import dataclass

from application.common.base_exceptions import ApplicationError


@dataclass(eq=False)
class InvalidResetPasswordToken(ApplicationError):
    @property
    def title(self) -> str:
        return f"Invalid Reset Password Token"
