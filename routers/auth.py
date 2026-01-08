from fastapi import APIRouter,HTTPException,Depends
from sqlmodel import Session,select

from database import get_session
from models.user import User
from models.refresh_token import RefreshToken
from schemas.auth import TokenResponse,RefreshRequest
from schemas.auth import SignupRequest

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime,timedelta
import secrets
import os

router = APIRouter(prefix="/auth",tags=["auth"])

# FOR HASHED PASSWORD

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
    )


def hash_password(password :str) -> str:
    if not password:
        raise ValueError("Password Cannot be empty.")
    return pwd_context.hash(password)

# For VERIFY HASHED PASSWORD

def verify_password(password :str,hashed_password :str) -> bool:
    return pwd_context.verify(password, hashed_password)


# JWT CONFIGURATION

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM","HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


# TOKEN CREATION FUNCTION

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# CREATE REFRESH TOKEN 

def create_refresh_token() -> str:
    return secrets.token_urlsafe(64)


# SIGNUP ENDPOINT

@router.post("/signup")
def signup(
    data: SignupRequest,
    session:Session = Depends(get_session)
):
    
    existing_user = session.exec(select(User).where(User.email==data.email)).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail= "Email already Registered."
        )
    
    user = User(
        email = data.email,
        hashed_password= hash_password(data.password)
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return {"message": "User created successfully"}




# LOGIN ENDPOINT

@router.post("/login")
def login(
    email : str,
    password : str,
    session : Session = Depends(get_session)
):
    
    user = session.exec(select(User).where(User.email==email)).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail= "Invalid credentials."
        )
    
    if not verify_password(password,user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail= "Invalid credentials."
        )
    

    access_token = create_access_token(
        {"sub":str(user.id)}
    )


    refresh_token_value = create_refresh_token()

    db_refresh_token = RefreshToken(
        token = refresh_token_value,
        user_id = user.id
    )

    session.add(db_refresh_token)
    session.commit()
    session.refresh(db_refresh_token)

    return TokenResponse(
        access_token = access_token,
        refresh_token = refresh_token_value
    )


# REFRESH TOKEN ENDPOINT

@router.post("/refresh")
def refresh_access_token(
    data : RefreshRequest,
    session : Session = Depends(get_session)
):
    
    db_token = session.exec(
        select(RefreshToken).where(RefreshToken.token == data.refresh_token, RefreshToken.is_revoked == False)
    ).first()

    if not db_token:
        raise HTTPException(
            status_code=401,
            detail = "Invalid Refresh token"
        )
    
    new_access_token = create_access_token(
        {"sub" : str(db_token.user_id)}
    )

    db_token.is_revoked = True

    new_refresh_token = create_refresh_token()

    new_db_token = RefreshToken(
        token = new_refresh_token,
        user_id = db_token.user_id,
    )


    session.add(new_db_token)
    session.commit()


    return TokenResponse(
        access_token = new_access_token,
        refresh_token = new_refresh_token,
    )

