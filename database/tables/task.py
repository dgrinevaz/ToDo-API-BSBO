from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from contracts.tasks import TaskStatus
from database.database import database_context

class Task(database_context):
    __tablename__ = "tasks"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True)

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
        nullable=False,
        default=TaskStatus.Pending)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False)

    deadline_at = Column(
        DateTime(timezone=True),
        nullable=False)

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True)

    owner = relationship(
        "User",
        back_populates="tasks"
    )

def __repr__(self) -> str:
    return f"<Task(id={self.id}, title='{self.title}', quadrant='{self.quadrant}')>"

def to_dict(self) -> dict:
    return {
    "id": self.id,
    "user_id": self.user_id,
    "title": self.title,
    "description": self.description,
    "quadrant": self.quadrant,
    "status": self.status,
    "created_at": self.created_at,
    "completed_at": self.completed_at
    }