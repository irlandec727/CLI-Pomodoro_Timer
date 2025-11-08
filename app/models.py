# app/models.py
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Boolean
from .db import Base, engine


class PomodoroSession(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    completed = Column(Boolean, default=True, nullable=False)
    accumulated_pause_seconds = Column(Integer, default=0, nullable=False)

    def __repr__(self) -> str:
        return (
            f"<PomodoroSession id={self.id} "
            f"duration={self.duration_minutes} "
            f"completed={self.completed}>"
        )


# создаём таблицу, если её ещё нет
Base.metadata.create_all(bind=engine)

