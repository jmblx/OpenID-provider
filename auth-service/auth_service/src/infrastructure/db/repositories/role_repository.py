import logging
from typing import Sequence

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from application.common.interfaces.role_repo import RoleRepository
from domain.entities.client.model import Client
from domain.entities.client.value_objects import ClientID
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
        role = await self.session.get(Role, role_id)
        return role

    async def get_roles_by_ids(self, role_ids: list[RoleID]) -> Sequence[Role]:
        result = await self.session.execute(
            sa.select(Role).where(Role.id.in_(role_ids))
        )
        roles = result.scalars().all()
        return roles

    async def get_roles_by_client_id(self, client_id: int, order_by_id: bool = False) -> Sequence[Role]:
        query = sa.select(Role).where(Role.client_id == client_id)
        if order_by_id:
            query = query.order_by(Role.id)
        result = await self.session.execute(
            query
        )
        roles = result.scalars().all()
        return roles

    async def get_base_client_roles(self, client_id: ClientID) -> list[Role]:
        stmt = (
            sa.select(Role)
            .where(Role.client_id == client_id)
            .where(Role.is_base == True)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_user_roles_by_client_id(
        self, user_id: UserID, client_id: ClientID
    ) -> list[Role]:
        stmt = (
            sa.select(Role)
            .join(
                user_role_association,
                Role.id == user_role_association.c.role_id,
            )
            .join(User, user_role_association.c.user_id == User.__table__.c.id)
            .join(Client, Role.client_id == Client.id)
            .where(User.id == user_id)
            .where(Client.id == int(client_id))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
