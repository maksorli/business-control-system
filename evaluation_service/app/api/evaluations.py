from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import datetime

from app.core.database import get_session
from app.repositories.evaluation_repository import EvaluationRepository
from app.schemas.evaluation import EvaluationCreate, EvaluationRead

router = APIRouter(prefix="/evaluations", tags=["Evaluations"])


@router.post("/", response_model=EvaluationRead, status_code=status.HTTP_201_CREATED)
async def create_evaluation(
    data: EvaluationCreate,
    session: AsyncSession = Depends(get_session)
):
    repo = EvaluationRepository(session)
    return await repo.create(data)


@router.get("/me/{user_id}", response_model=list[EvaluationRead])
async def get_user_evaluations(
    user_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    repo = EvaluationRepository(session)
    return await repo.get_by_user(user_id)


@router.get("/average/quarter/{user_id}")
async def get_user_quarter_avg(
    user_id: UUID,
    year: int = Query(..., description="Год, например 2024"),
    quarter: int = Query(..., ge=1, le=4, description="Квартал: 1-4"),
    session: AsyncSession = Depends(get_session)
):
    repo = EvaluationRepository(session)
    return await repo.get_quarter_average(user_id, year, quarter)


@router.post("/average/department")
async def get_department_avg(
    user_ids: list[UUID],  # список ID сотрудников отдела
    session: AsyncSession = Depends(get_session)
):
    repo = EvaluationRepository(session)
    return await repo.get_department_average(user_ids)
