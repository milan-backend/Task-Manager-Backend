from sqlmodel import SQLModel
from typing import Optional



class ProjectCreate(SQLModel):
    name : str
    description : Optional[str] = None

class ProjectResponse(SQLModel):
    id : int 
    name : str
    description : Optional[str] = None
    owner_id : int