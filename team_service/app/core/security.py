from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.schemas.current_user import CurrentUser
from typing import Optional
import os
from uuid import UUID
from fastapi.security import HTTPBearer


SECRET_KEY = os.getenv("JWT_SECRET")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET environment variable is not set.")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

 
oauth2_scheme = HTTPBearer()


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
    except JWTError:
        return None

async def get_current_user(token: str = Depends(oauth2_scheme)) -> CurrentUser:
    payload = decode_token(token.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")
    role = payload.get("role")
    team_id = payload.get("team_id")

    if not user_id or not role:
        raise HTTPException(status_code=403, detail="Missing token fields")

    return CurrentUser(
        id=UUID(user_id),
        role=role,
        team_id=UUID(team_id) if team_id else None
    )

