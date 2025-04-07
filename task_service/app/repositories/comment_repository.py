from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from app.models.comment import Comment
from app.schemas.comment import CommentCreate


class CommentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: CommentCreate) -> Comment:
        comment = Comment(**data.model_dump())
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def get_by_id(self, comment_id: UUID) -> Comment | None:
        result = await self.session.execute(
            select(Comment).where(Comment.id == comment_id)
        )
        return result.scalars().first()

    async def delete(self, comment_id: UUID) -> bool:
        comment = await self.get_by_id(comment_id)
        if not comment:
            return False

        await self.session.delete(comment)
        await self.session.commit()
        return True

    async def list_by_task(self, task_id: UUID) -> list[Comment]:
        result = await self.session.execute(
            select(Comment).where(Comment.task_id == task_id)
        )
        return result.scalars().all()
