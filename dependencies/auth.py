from fastapi import Depends,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from jose import jwt,JWTError
from sqlmodel import Session,select

from database import get_session
from models.user import User
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM","HS256")

security = HTTPBearer()


def get_current_user(
        credentials : HTTPAuthorizationCredentials = Depends(security),
        session : Session = Depends(get_session)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id : str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code= 401,
                detail = "Invalid token."
            )
        
        user = session.exec(
            select(User).where(User.id == int(user_id))
        ).first()


        if not user:
            raise HTTPException(
                status_code = 401,
                detail = "User not found."
            )
        
        return user
    
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail= "Invalid token or expired token."
        )
            
