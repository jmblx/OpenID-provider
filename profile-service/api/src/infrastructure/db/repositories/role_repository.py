from sqlalchemy.ext.asyncio import AsyncSession

from application.role.interfaces.repo import RoleRepository
from domain.entities.role.model import Role
from domain.entities.role.value_objects import RoleID


class RoleRepositoryImpl(RoleRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, role: Role) -> RoleID:
        """
        Сохраняет объект роли (Role) в базе данных.
        """
        role = await self.session.merge(role)
        await self.session.flush()
        return role.id
