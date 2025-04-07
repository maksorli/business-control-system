from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: TaskCreate) -> Task:
        task = Task(**data.model_dump())
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_by_id(self, task_id: UUID) -> Task | None:
        result = await self.session.execute(
            select(Task).where(Task.id == task_id)
        )
        return result.scalars().first()

    async def update(self, task_id: UUID, data: TaskUpdate) -> Task | None:
        task = await self.get_by_id(task_id)
        if not task:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)

        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete(self, task_id: UUID) -> bool:
        task = await self.get_by_id(task_id)
        if not task:
            return False

        await self.session.delete(task)
        await self.session.commit()
        return True

    async def list_by_team(self, team_id: UUID) -> list[Task]:
        result = await self.session.execute(
            select(Task).where(Task.team_id == team_id)
        )
        return result.scalars().all()
