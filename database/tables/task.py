from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database.database import database_context

class Task(database_context):
    __tablename__ = "tasks"

    id = Column(
    Integer,
    primary_key=True,
    index=True,
    autoincrement=True)

    title = Column(
    Text,
    nullable=False)

    description = Column(
    Text,
    nullable=True)

    quadrant = Column(
    String(2),
    nullable=False)

    status = Column(
    Text,
    nullable=False)

    created_at = Column(
    DateTime(timezone=True),
    server_default=func.now(),
    nullable=False)

    completed_at = Column(
    DateTime(timezone=True),
    nullable=True)

def __repr__(self) -> str:
    return f"<Task(id={self.id}, title='{self.title}', quadrant='{self.quadrant}')>"

def to_dict(self) -> dict:
    return {
    "id": self.id,
    "title": self.title,
    "description": self.description,
    "quadrant": self.quadrant,
    "status": self.status,
    "created_at": self.created_at,
    "completed_at": self.completed_at
    }