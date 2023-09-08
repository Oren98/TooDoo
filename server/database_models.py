from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date, DateTime, Enum
from sqlalchemy.dialects.postgresql import ARRAY
from custom_types import Priority, Status
from database import base


class Users(base):
    """
    Users table ORM
    """
    __tablename__ = 'users'

    id = Column("id", Integer, primary_key=True, nullable=False, index=True)
    name = Column("name", String(50), nullable=False, index=True, unique=True)
    password = Column("password", String(160), nullable=False)
    mail = Column("mail", String(255), nullable=False)


class Todos(base):
    """
    Todos table ORM
    """
    __tablename__ = 'todos'

    id = Column("id", Integer, primary_key=True, nullable=False, index=True)
    title = Column("title", Text, nullable=False, index=True)
    description = Column("description", Text)
    deadline = Column("deadline", Date, nullable=False)
    priority = Column("priority", Enum(Priority), nullable=False, default=Priority.medium)
    reminder = Column("reminder", DateTime)
    tags = Column("tags", ARRAY(String, dimensions=1))
    creator = Column("creator", Integer, ForeignKey("users.id"), nullable=False)
    status = Column("status", Enum(Status), nullable=False, default=Status.ready)


class UserTodoRelations(base):
    """
    UserTodoRelations table ORM
    """
    __tablename__ = 'user_todo_relation'

    user_id = Column("user_id", Integer, ForeignKey("users.id"), nullable=False, primary_key=True)
    todo_id = Column("todo_id", Integer, ForeignKey("todos.id"), nullable=False, primary_key=True)