from sqlmodel import SQLModel

class TokenResponse(SQLModel):
    access_token : str 
    refresh_token : str
    token_type : str = "Bearer"


class RefreshRequest(SQLModel):
    refresh_token : str