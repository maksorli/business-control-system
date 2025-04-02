from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.models.team import Team
from uuid import UUID
from typing import Optional
from datetime import datetime
from typing import List

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.email == email, User.is_deleted == False)
        )
        return result.scalar()
    
    async def get_all_users(self) -> List[User]:
        result = await self.session.execute(
            select(User).where(User.is_deleted == False)
        )
        return result.scalars().all()


    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        return await self.session.get(User, user_id)

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def soft_delete(self, user: User):
        user.is_deleted = True
        user.deleted_at = datetime.utcnow()
        await self.session.commit()

    async def restore(self, user: User):
        user.is_deleted = False
        user.deleted_at = None
        await self.session.commit()

    async def update(self, user: User, data: dict):
        for key, value in data.items():
            setattr(user, key, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def get_team_by_invite_code(self, code: str) -> Optional[Team]:
        result = await self.session.execute(
            select(Team).where(Team.invite_code == code)
        )
        return result.scalar_one_or_none()