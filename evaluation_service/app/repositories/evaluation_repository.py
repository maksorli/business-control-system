from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from uuid import UUID
from datetime import datetime
from app.models.evaluation import TaskEvaluation
from app.schemas.evaluation import EvaluationCreate


class EvaluationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: EvaluationCreate) -> TaskEvaluation:
        evaluation = TaskEvaluation(**data.model_dump())
        self.session.add(evaluation)
        await self.session.commit()
        await self.session.refresh(evaluation)
        return evaluation

    async def get_by_user(self, user_id: UUID) -> list[TaskEvaluation]:
        stmt = select(TaskEvaluation).where(TaskEvaluation.assignee_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_quarter_average(self, user_id: UUID, year: int, quarter: int) -> dict[str, float]:
        # квартал: 1→(1–3), 2→(4–6), 3→(7–9), 4→(10–12)
        month_ranges = {
            1: (1, 3),
            2: (4, 6),
            3: (7, 9),
            4: (10, 12),
        }
        start_month, end_month = month_ranges.get(quarter, (1, 3))

        stmt = (
            select(
                func.avg(TaskEvaluation.score_speed),
                func.avg(TaskEvaluation.score_quality),
                func.avg(TaskEvaluation.score_completeness),
            )
            .where(
                TaskEvaluation.assignee_id == user_id,
                extract("year", TaskEvaluation.created_at) == year,
                extract("month", TaskEvaluation.created_at).between(start_month, end_month)
            )
        )
        result = await self.session.execute(stmt)
        avg_speed, avg_quality, avg_completeness = result.one_or_none()
        return {
            "avg_speed": avg_speed or 0.0,
            "avg_quality": avg_quality or 0.0,
            "avg_completeness": avg_completeness or 0.0,
        }

    async def get_department_average(self, department_user_ids: list[UUID]) -> dict[str, float]:
        if not department_user_ids:
            return {"avg_speed": 0.0, "avg_quality": 0.0, "avg_completeness": 0.0}

        stmt = (
            select(
                func.avg(TaskEvaluation.score_speed),
                func.avg(TaskEvaluation.score_quality),
                func.avg(TaskEvaluation.score_completeness),
            )
            .where(TaskEvaluation.assignee_id.in_(department_user_ids))
        )
        result = await self.session.execute(stmt)
        avg_speed, avg_quality, avg_completeness = result.one_or_none()
        return {
            "avg_speed": avg_speed or 0.0,
            "avg_quality": avg_quality or 0.0,
            "avg_completeness": avg_completeness or 0.0,
        }
