from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
import os
import logging
from fastapi import Depends, HTTPException 
from fastapi.security import OAuth2PasswordBearer

from app.repositories.user_repository import UserRepository
from app.core.dependencies import get_user_repository


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("JWT_SECRET")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET environment variable is not set.")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=60))
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
         "sub": str(data.get("sub", "")),  # если есть user_id
        })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        logging.warning(f"Invalid JWT token: {e}")
        return None
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")



async def get_current_user(
    token: str = Depends(oauth2_scheme),
    repo: UserRepository = Depends(get_user_repository),
):
    payload = decode_token(token)
    user_id = payload.get("sub") if payload else None

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user