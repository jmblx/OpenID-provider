from abc import abstractmethod, ABC
from typing import Optional, TypedDict

from domain.entities.user.model import User
from domain.entities.user.value_objects import UserID, Email


class UserReader(ABC): ...
