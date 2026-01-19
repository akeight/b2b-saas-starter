from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from app.models.task import TaskStatus

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None

class TaskStatusUpdate(BaseModel):
    status: TaskStatus

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    org_id: str
    created_at: datetime
    updated_at: datetime
    created_by: str

    class Config:
        from_attributes = True