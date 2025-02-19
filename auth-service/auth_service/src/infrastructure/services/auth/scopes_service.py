from collections import defaultdict

from application.auth.scopes_service import ScopesService
from domain.entities.role.model import Role


class ScopesServiceImpl(ScopesService):
    def calculate_full_user_scopes_for_client(
        self, roles: list[Role]
    ) -> list[str]:
        """
        Вычисляет полный список разрешений на основе всех ролей.

        Если хотя бы в одной роли установлен бит 1, то он остаётся 1 в итоговом результате.
        Возвращает список строковых битовых масок в формате "scope:bitmask".
        """
        merged_permissions = defaultdict(int)

        for role in roles:
            for scope, bitmask in role.base_scopes.value.items():
                merged_permissions[scope] |= bitmask

        return [
            f"{scope}:{bitmask:04b}"
            for scope, bitmask in merged_permissions.items()
        ]
