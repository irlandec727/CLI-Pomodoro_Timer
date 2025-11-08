# app/api.py
from datetime import datetime
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import PomodoroSession

app = FastAPI(title="Pomodoro API")


class SessionOut(BaseModel):
    id: int
    started_at: datetime
    duration_minutes: int
    completed: bool
    accumulated_pause_seconds: int

    class Config:
        orm_mode = True


@app.get("/sessions", response_model=List[SessionOut])
def list_sessions(db: Session = Depends(get_db)):
    """Список всех сессий, последние сверху."""
    sessions = (
        db.query(PomodoroSession)
        .order_by(PomodoroSession.id.desc())
        .all()
    )
    return sessions


@app.get("/sessions/{session_id}", response_model=SessionOut)
def get_session(session_id: int, db: Session = Depends(get_db)):
    """Получить одну сессию по id."""
    session = db.get(PomodoroSession, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
