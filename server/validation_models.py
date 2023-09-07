from typing import List
from pydantic import BaseModel
from custom_types import Priority, Status
from datetime import date, datetime


class ValidUser(BaseModel):
    id: int
    name: str
    password: str
    mail: str


class ValidUserChanges(BaseModel):
    id: int
    name: str | None
    password: str | None
    mail: str | None


class ValidTodo(BaseModel):
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
    id: int
    title: str | None
    description: str | None
    deadline: date | None
    priority: Priority | None
    reminder: datetime | None
    status: Status | None
    tags: List[str] | None


class ValidUserTodoRelation(BaseModel):
    user_id: int
    todo_id: int

