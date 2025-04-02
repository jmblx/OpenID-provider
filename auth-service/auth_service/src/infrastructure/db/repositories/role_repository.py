import logging
from typing import Sequence

import sqlalchemy as sa
from sqlalchemy import and_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from application.common.interfaces.role_repo import RoleRepository
from domain.entities.resource_server.model import ResourceServer
from domain.entities.resource_server.value_objects import ResourceServerID, ResourceServerType
from domain.entities.role.model import Role
from domain.entities.role.value_objects import RoleID
from domain.entities.user.model import User
from domain.entities.user.value_objects import UserID
from infrastructure.db.models.secondary import user_role_association

logger = logging.getLogger(__name__)


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

    async def get_by_id(self, role_id: RoleID) -> Role | None:
        stmt = (
            select(Role)
            .where(and_(Role.id == role_id), Role.is_active == True)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_roles_by_ids(self, role_ids: list[RoleID]) -> Sequence[Role]:
        result = await self.session.execute(
            sa.select(Role).where(and_(Role.id.in_(role_ids), Role.is_active == True))
        )
        roles = result.scalars().all()
        return roles

    async def get_roles_by_rs_id(
        self, rs_id: int, order_by_id: bool = False
    ) -> Sequence[Role]:
        query = sa.select(Role).where(and_(Role.rs_id == rs_id), Role.is_active == True)
        if order_by_id:
            query = query.order_by(Role.id)
        result = await self.session.execute(query)
        roles = result.scalars().all()
        return roles

    async def get_base_rs_roles(self, rs_id: ResourceServerID) -> list[Role]:
        stmt = (
            sa.select(Role)
            .where(and_(Role.rs_id == rs_id, Role.is_base == True, Role.is_active == True))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_user_roles_by_rs_ids(
            self, user_id: UserID, rs_ids: Sequence[ResourceServerID]
    ) -> list[Role]:
        stmt = text("""
            SELECT r.* FROM role r
            JOIN user_role_association ura ON r.id = ura.role_id
            JOIN "user" u ON ura.user_id = u.id
            JOIN resource_server rs ON r.rs_id = rs.id
            WHERE u.id = :user_id
              AND rs.id = ANY(:rs_ids)
              AND rs.type = :rs_type
              AND r.is_active = TRUE
        """)

        result = await self.session.execute(stmt, {
            "user_id": str(user_id.value),
            "rs_ids": rs_ids,
            "rs_type": ResourceServerType.RBAC_BY_AS.value,
        })

        return result.mappings().all()

    async def delete_role(self, role: Role) -> None:
        role.is_active = True
