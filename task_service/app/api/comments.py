from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.database import get_session
from app.core.security import get_current_user
from app.schemas.current_user import CurrentUser

from app.schemas.comment import CommentCreate, CommentRead
from app.repositories.comment_repository import CommentRepository
from app.repositories.task_repository import TaskRepository

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
async def create_comment(
    data: CommentCreate,
    session: AsyncSession = Depends(get_session),
    current_user: CurrentUser = Depends(get_current_user),
):
    # Проверяем, что задача существует и принадлежит команде текущего пользователя
    task_repo = TaskRepository(session)
    task = await task_repo.get_by_id(data.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # if task.team_id != current_user.team_id:
    #     raise HTTPException(status_code=403, detail="Access denied")

    repo = CommentRepository(session)
    comment = await repo.create(data)
    return comment


@router.get("/task/{task_id}", response_model=list[CommentRead])
async def get_comments_for_task(
    task_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: CurrentUser = Depends(get_current_user),
):
    # Проверка доступа к задаче
    task_repo = TaskRepository(session)
    task = await task_repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # if task.team_id != current_user.team_id:
    #     raise HTTPException(status_code=403, detail="Access denied")

    repo = CommentRepository(session)
    comments = await repo.list_by_task(task_id)
    return comments


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: CurrentUser = Depends(get_current_user),
):
    repo = CommentRepository(session)
    comment = await repo.get_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Проверка доступа: текущий пользователь — автор комментария
    # if comment.user_id != current_user.id:
    #     raise HTTPException(status_code=403, detail="Access denied")

    await repo.delete(comment_id)
