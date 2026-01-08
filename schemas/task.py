from sqlmodel import SQLModel
from typing import Optional
from core.enums import TaskStatus

class TaskCreate(SQLModel):
    project_id : int
    title : str
    description : Optional[str] = None


class TaskResponse(SQLModel):
    id : int
    title : str
    description : Optional[str] = None
    status : str
    project_id : int
    created_by : int
    assigned_to : Optional[int] = None


class TaskUpdate(SQLModel):
    status : Optional[TaskStatus] = None
    assigned_to : Optional[int] = None




