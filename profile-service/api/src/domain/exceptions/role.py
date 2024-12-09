from dataclasses import dataclass

from domain.common.exceptions.base import DomainError


@dataclass(eq=False)
class InvalidPermissionsError(DomainError):
    description: str

    @property
    def title(self) -> str:
        return f"Invalid Permissions: {self.description}"


# @dataclass(eq=False)
# class InvalidRoleIDError(DomainError):
#     role_id: int
#
#     @property
#     def title(self) -> str:
#         return f"Invalid Role ID: {self.role_id}"

# @dataclass(eq=False)
# class InvalidRoleNameError(DomainError):
#     @property
#     def title(self) -> str:
#         return ""
