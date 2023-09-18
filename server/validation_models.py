from datetime import date, datetime
from typing import List

from pydantic import BaseModel

from custom_types import Priority, Status


class ValidUser(BaseModel):
    """
    User validation object. fields for creating a user.
    """

    name: str
    password: str
    mail: str


class ValidUserChanges(BaseModel):
    """
    User changes validation object. fields for changing a user.
    """

    id: int
    name: str | None
    password: str | None
    mail: str | None


class ValidTodo(BaseModel):
    """
    Todo validation object. fields for creating a todo.
    """

    id: int
    title: str
    description: str | None
    deadline: date
    priority: Priority
    reminder: datetime | None
    status: Status
    tags: List[str] | None
    creator: int


class ValidTodoChanges(BaseModel):
    """
    Todo changes validation object. fields for changing a todo.
    """

    id: int
    title: str | None
    description: str | None
    deadline: date | None
    priority: Priority | None
    reminder: datetime | None
    status: Status | None
    tags: List[str] | None
