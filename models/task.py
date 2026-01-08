from sqlmodel import SQLModel,Field
from typing import Optional
from core.enums import TaskStatus


class Task(SQLModel,table=True):

    id : Optional[int] = Field(default=None,primary_key=True)

    title : str
    description : Optional[str] = Field(default=None)
    status : TaskStatus = Field(default=TaskStatus.TODO)

    project_id : int = Field(foreign_key="project.id")
    created_by : int = Field(foreign_key="user.id")
    assigned_to : Optional[int] = Field(default=None,foreign_key="user.id")