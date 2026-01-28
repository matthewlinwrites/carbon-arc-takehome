from datetime import datetime
from pydantic import BaseModel


class Task(BaseModel):
    id: str
    title: str
    completed: bool = False
    created_at: datetime
    updated_at: datetime


class ActivityLog(BaseModel):
    id: str
    task_id: str
    action: str  # "created", "completed", "deleted", "updated"
    timestamp: datetime
    old_value: str | None = None
    new_value: str | None = None


class TaskStats(BaseModel):
    total: int
    completed: int
    pending: int
