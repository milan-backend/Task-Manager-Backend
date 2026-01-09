from pydantic import BaseModel
from core.enums import TaskStatus
from typing import Optional

class TaskCreate(BaseModel):
    project_id : int
    title : str
    description : Optional[str] = None


class TaskResponse(BaseModel):
    id : int
    title : str
    description : Optional[str] = None
    status : str
    project_id : int
    created_by : int
    assigned_to : Optional[int] = None


class TaskUpdate(BaseModel):
    status : Optional[TaskStatus] = None
    assigned_to : Optional[int] = None




