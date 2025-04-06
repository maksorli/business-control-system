from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate
from uuid import UUID


class DepartmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: DepartmentCreate) -> Department:
        department = Department(**data.model_dump())
        self.session.add(department)
        await self.session.commit()
        await self.session.refresh(department)
        return department

    async def get_by_id(self, department_id: UUID) -> Department | None:
        result = await self.session.execute(
            select(Department).where(Department.id == department_id)
        )
        return result.scalars().first()

    async def update(self, department_id: UUID, data: DepartmentUpdate) -> Department | None:
        department = await self.get_by_id(department_id)
        if not department:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(department, field, value)

        await self.session.commit()
        await self.session.refresh(department)
        return department

    async def delete(self, department_id: UUID) -> bool:
        department = await self.get_by_id(department_id)
        if not department:
            return False

        await self.session.delete(department)
        await self.session.commit()
        return True
