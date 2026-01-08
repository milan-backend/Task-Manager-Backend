from sqlmodel import SQLModel,Field
from typing import Optional

class ProjectMember(SQLModel, table=True):
    id : Optional[int] = Field(default=None,primary_key=True)

    project_id : int = Field(foreign_key="project.id")
    user_id : int = Field(foreign_key="user.id")
