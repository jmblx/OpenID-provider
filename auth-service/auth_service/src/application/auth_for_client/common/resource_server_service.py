from abc import ABC, abstractmethod

from domain.entities.user.model import User


class ResourceServerService(ABC):

    async def add_rs_by_ids_to_user(self, user, param):
        pass
