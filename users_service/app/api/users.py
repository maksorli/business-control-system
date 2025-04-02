from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_session
from app.repositories.user_repository import UserRepository
from app.services import user_service
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.core.security import create_access_token, get_current_user
from typing import List
router = APIRouter(prefix="/users", tags=["Users"])

def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session)

@router.get("/", response_model=List[UserOut])
async def get_all_users(repo: UserRepository = Depends(get_user_repository)):
    users = await repo.get_all_users()
    return users

@router.post("/register", response_model=UserOut)
async def register_user(
    data: UserCreate,
    repo: UserRepository = Depends(get_user_repository),
):
    return await user_service.register_user(data, repo)

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    repo: UserRepository = Depends(get_user_repository),
):
    user = await user_service.authenticate_user(form_data.username, form_data.password, repo)
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.delete("/{user_id}")
async def delete_user(
    user_id: UUID,
    repo: UserRepository = Depends(get_user_repository),
):
    await user_service.delete_user(user_id, repo)
    return {"detail": "User soft-deleted"}

@router.post("/{user_id}/restore")
async def restore_user(
    user_id: UUID,
    repo: UserRepository = Depends(get_user_repository),
):
    await user_service.restore_user(user_id, repo)
    return {"detail": "User restored"}

 

@router.put("/me", response_model=UserOut)
async def update_me(
    data: UserUpdate,
    current_user=Depends(get_current_user),
    repo: UserRepository = Depends(get_user_repository),
):
    return await user_service.update_user(current_user.id, data, repo)