from abc import ABC, abstractmethod

from domain.entities.role.model import Role


class ScopesService(ABC):
    @abstractmethod
    def calculate_full_user_scopes_for_client(
        self, roles: list[Role]
    ) -> list[str]: ...
