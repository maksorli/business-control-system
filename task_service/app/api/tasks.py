from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.database import get_session
from app.core.security import get_current_user
from app.core.permissions import require_admin_user
from app.utils.validate_team import validate_team_id

from app.schemas.task import TaskCreate, TaskUpdate, TaskRead
from app.schemas.current_user import CurrentUser
from app.repositories.task_repository import TaskRepository

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    data: TaskCreate,
    session: AsyncSession = Depends(get_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    #await validate_team_id(str(data.team_id), current_user.token) нужна ли команда для таски?

    # if data.team_id != current_user.team_id:
    #     raise HTTPException(status_code=403, detail="Access denied to this team")

    repo = TaskRepository(session)
    task = await repo.create(data)
    return task


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    repo = TaskRepository(session)
    task = await repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # if task.team_id != current_user.team_id:
    #     raise HTTPException(status_code=403, detail="Access denied")
    return task


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: UUID,
    data: TaskUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    repo = TaskRepository(session)
    task = await repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # if task.team_id != current_user.team_id:
    #     raise HTTPException(status_code=403, detail="Access denied")

    updated = await repo.update(task_id, data)
    return updated


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: CurrentUser = Depends(require_admin_user)
):
    repo = TaskRepository(session)
    task = await repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # if task.team_id != current_user.team_id:
    #     raise HTTPException(status_code=403, detail="Access denied")

    deleted = await repo.delete(task_id)
    if not deleted:
        raise HTTPException(status_code=400, detail="Delete failed")
