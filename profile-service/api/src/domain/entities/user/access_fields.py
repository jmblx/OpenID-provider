from typing import TypedDict

from domain.entities.user.value_objects import UserID


class UserAccessFields(TypedDict):
    id: UserID
