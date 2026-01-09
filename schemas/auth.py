from pydantic import BaseModel,EmailStr

class TokenResponse(BaseModel):
    access_token : str 
    refresh_token : str
    token_type : str = "Bearer"


class RefreshRequest(BaseModel):
    refresh_token : str


class SignupRequest(BaseModel):
    email : EmailStr
    password : str