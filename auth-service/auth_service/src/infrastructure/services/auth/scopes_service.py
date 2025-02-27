from collections import defaultdict

from application.auth_as.common.scopes_service import ScopesService
from domain.entities.role.model import Role


class ScopesServiceImpl(ScopesService):
    def calculate_full_user_scopes_for_client(
        self, roles: list[Role] | list[dict]
    ) -> list[str]:
        """
        Вычисляет полный список разрешений на основе всех ролей.

        Если хотя бы в одной роли установлен бит 1, то он остаётся 1 в итоговом результате.
        Работает как с list[Role], так и с list[dict].
        """

        merged_permissions = defaultdict(int)

        for role in roles:
            base_scopes = (
                role.base_scopes.value
                if isinstance(role, Role) else role["base_scopes"]
            )
            for scope, bitmask in base_scopes.items():
                merged_permissions[scope] |= bitmask

        return [
            f"{scope}:{bitmask:04b}"
            for scope, bitmask in merged_permissions.items()
        ]
