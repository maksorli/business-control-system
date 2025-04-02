from fastapi import HTTPException, Depends, status
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password, verify_password,oauth2_scheme
from app.core.dependencies import get_user_repository
from app.repositories.user_repository import UserRepository
from uuid import UUID
from app.core.security import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt

async def register_user(data: UserCreate, repo: UserRepository) -> User:
    existing = await repo.get_by_email(data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

     
    if data.invite_code:
        team = await repo.get_team_by_invite_code(data.invite_code)
        if not team:
            raise HTTPException(status_code=404, detail="Invalid invite code")
   
        
    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
        invite_code = data.invite_code,
        role=data.role,
    )
    return await repo.create(user)

async def authenticate_user(email: str, password: str, repo: UserRepository) -> User:
    user = await repo.get_by_email(email)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

async def delete_user(user_id: UUID, repo: UserRepository):
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await repo.soft_delete(user)

async def restore_user(user_id: UUID, repo: UserRepository):
    user = await repo.get_by_id(user_id)
    if not user or not user.is_deleted:
        raise HTTPException(status_code=404, detail="User not found or not deleted")
    await repo.restore(user)

async def update_user(user_id: UUID, data: UserUpdate, repo: UserRepository):

    team_id = None
    if data.invite_code:
        team = await repo.get_team_by_invite_code(data.invite_code)
        if not team:
            raise HTTPException(status_code=404, detail="Invalid invite code")


    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = data.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password_hash"] = hash_password(update_data.pop("password"))

    return await repo.update(user, update_data)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    repo: UserRepository = Depends(get_user_repository),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate token")

    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user