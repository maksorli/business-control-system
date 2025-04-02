from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
 
from app.models.team import Team
from uuid import UUID
from typing import Optional
from datetime import datetime
from typing import List

class TeamRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_teams(self) -> List[Team]:
        result = await self.session.execute(
            select(Team).where(Team.is_deleted == False)
        )
        return result.scalars().all()

    async def get_team_by_id(self, team_id: UUID) -> Optional[Team]:
        result = await self.session.execute(
            select(Team).where(Team.id == team_id)
        )
        return result.scalar_one_or_none()

    async def get_team_by_invite_code(self, code: str) -> Optional[Team]:
        result = await self.session.execute(
            select(Team).where(Team.invite_code == code)
        )
        return result.scalar_one_or_none()

    async def create_team(self, name: str, invite_code: str) -> Team:
        new_team = Team(name=name, invite_code=invite_code)
        self.session.add(new_team)
        await self.session.commit()
        await self.session.refresh(new_team)
        return new_team

    async def delete_team(self, team_id: UUID) -> None:
        result = await self.session.execute(
            select(Team).where(Team.id == team_id)
        )
        team = result.scalar_one_or_none()
        if team:
            team.is_deleted = True
            team.deleted_at = datetime.utcnow()
            await self.session.commit()