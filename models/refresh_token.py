from sqlmodel import SQLModel,Field
from typing import Optional
from datetime import datetime

class RefreshToken(SQLModel,table=True):

    id : Optional[int] = Field(default=None,primary_key=True)

    token : str = Field(unique=True,index=True)
    user_id : str = Field(foreign_key="user.id")

    is_revoked : bool = Field(default=False)

    created_at : datetime = Field(default_factory=datetime.utcnow)