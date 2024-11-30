from dataclasses import dataclass

from domain.exceptions.user_vo import InvalidRoleIDError, InvalidRoleNameError
from domain.exceptions.role import InvalidPermissionsError


@dataclass(frozen=True)
class RoleID:
    value: int
    _valid_values = (0, 1, 2)

    def __post_init__(self):
        if self.value not in self._valid_values:
            raise InvalidRoleIDError(
                "RoleID must be a valid int and refer to a valid role."
            )


@dataclass(frozen=True)
class RoleName:
    value: str
    _allowed_names = {"user", "admin"}

    def __post_init__(self):
        if self.value not in self._allowed_names:
            raise InvalidRoleNameError(
                "RoleName must be one of the allowed names."
            )


@dataclass(frozen=True)
class RolePermissions:
    value: dict[str, int]

    def __post_init__(self) -> None:
        """
        Проверка валидности значений в словаре.
        Убедитесь, что все значения - 4-значные побитовые числа.
        """
        if not isinstance(self.value, dict):
            raise TypeError("Permissions must be a dictionary")

        for key, permission in self.value.items():
            if not isinstance(key, str):
                raise TypeError(f"Key {key} must be a string")
            if not isinstance(permission, int) or not self._is_valid_bitwise(
                permission
            ):
                raise InvalidPermissionsError(
                    f"Permission value {permission} for key '{key}' is not a valid 4-bit number"
                )

    @staticmethod
    def _is_valid_bitwise(value: int) -> bool:
        """
        Проверяет, является ли число 4-значным побитовым числом (0-15).
        """
        return 0 <= value <= 15

    def get_permission(self, key: str) -> int:
        """
        Получает значение разрешения по ключу.
        """
        return self.value.get(key, 0)

    def set_permission(self, key: str, permission: int) -> "RolePermissions":
        """
        Возвращает новый объект с обновленным значением разрешения.
        """
        if not self._is_valid_bitwise(permission):
            raise InvalidPermissionsError(
                f"Permission value {permission} is not a valid 4-bit number"
            )
        new_permissions = dict(self.value)
        new_permissions[key] = permission
        return RolePermissions(new_permissions)

    def has_permission(self, key: str, bit: int) -> bool:
        """
        Проверяет, установлен ли определенный бит в значении разрешения по ключу.
        """
        if key not in self.value:
            return False
        return (self.value[key] & (1 << bit)) != 0

    def to_dict(self) -> dict[str, int]:
        """
        Возвращает словарь разрешений.
        """
        return self.value
