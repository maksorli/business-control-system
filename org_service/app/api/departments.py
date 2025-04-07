from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.utils.validate_team import validate_team_id
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentRead
from app.repositories.department_repository import DepartmentRepository
from app.core.database import get_session
from app.core.security import get_current_user  
from app.schemas.current_user import CurrentUser
from app.core.permissions import require_admin_user

router = APIRouter(prefix="/departments", tags=["departments"])


@router.post("/", response_model=DepartmentRead, status_code=status.HTTP_201_CREATED)
async def create_department(
    data: DepartmentCreate,
    session: AsyncSession = Depends(get_session),
    current_user: CurrentUser = Depends(require_admin_user)
): 
    if current_user.team_id:
        raise HTTPException(status_code=400, detail="User already in a team")
    await validate_team_id(str(data.team_id), current_user.token)
    repo = DepartmentRepository(session)
    department = await repo.create(data)
    return department


@router.get("/{department_id}", response_model=DepartmentRead)
async def get_department(
    department_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: CurrentUser = Depends(require_admin_user)
):
    if current_user.team_id:
        raise HTTPException(status_code=400, detail="User already in a team")
    repo = DepartmentRepository(session)
    department = await repo.get_by_id(department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@router.patch("/{department_id}", response_model=DepartmentRead)
async def update_department(
    department_id: UUID,
    data: DepartmentUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: CurrentUser = Depends(require_admin_user)
):
    if current_user.team_id:
        raise HTTPException(status_code=400, detail="User already in a team")
    repo = DepartmentRepository(session)
    department = await repo.update(department_id, data)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
    department_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: CurrentUser = Depends(require_admin_user)
):
    if current_user.team_id:
        raise HTTPException(status_code=400, detail="User already in a team")
    repo = DepartmentRepository(session)
    deleted = await repo.delete(department_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Department not found")
