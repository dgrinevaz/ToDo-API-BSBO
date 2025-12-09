from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from contracts.authorization import UserRole
from database.database import database_context

class User(database_context):
    __tablename__ = "users"

    id = Column(
    Integer,
    primary_key=True,
    index=True,
    autoincrement=True)

    username = Column(
    String(50),
    unique=True,
    nullable=False,
    index=True)

    email = Column(
    String(100),
    unique=True,
    nullable=False,
    index=True)

    password = Column(
    String(255),
    nullable=False)

    role = Column(
    Text,
    nullable=False,
    default=UserRole.USER)

    tasks = relationship(
    "Task",
    back_populates="owner",
    cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', role='{self.role.value}')>"
