from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.core.database import get_session
from app.core.security import get_current_user  # это JWT → DTO
from app.schemas.current_user import CurrentUser
from app.repositories.team_repository import TeamRepository
from app.schemas.team import TeamCreate, TeamOut, JoinTeamRequest
import random
import string
from app.core.permissions import require_admin_user
from app.core.security import oauth2_scheme
router = APIRouter(prefix="/teams", tags=["Teams"])


def get_team_repository(session: AsyncSession = Depends(get_session)) -> TeamRepository:
    return TeamRepository(session)


def generate_invite_code(length: int = 8) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


@router.get("/", response_model=List[TeamOut])
async def get_all_teams(repo: TeamRepository = Depends(get_team_repository)):
    return await repo.get_all_teams()


@router.post("/", response_model=TeamOut)
async def create_team(
    data: TeamCreate,
    current_user: CurrentUser = Depends(require_admin_user),
    repo: TeamRepository = Depends(get_team_repository),
):
    if current_user.team_id:
        raise HTTPException(status_code=400, detail="User already in a team")

    invite_code = generate_invite_code()
    new_team = await repo.create_team(data.name,data.description, invite_code)
 
    return new_team


@router.post("/join")
async def join_team(
    data: JoinTeamRequest,
    current_user: CurrentUser = Depends(get_current_user),
    repo: TeamRepository = Depends(get_team_repository),
):
    team = await repo.get_team_by_invite_code(data.invite_code)
    if not team:
        raise HTTPException(status_code=404, detail="Invalid invite code")

    # Здесь тоже нужно обновить user.team_id через user_service
    return {"detail": f"User joined team {team.name}", "team_id": str(team.id)}


@router.get("/{team_id}", response_model=TeamOut)
async def get_team_by_id(
    team_id: UUID,
    repo: TeamRepository = Depends(get_team_repository)
):
    team = await repo.get_team_by_id(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.delete("/{team_id}")
async def soft_delete_team(
    team_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    repo: TeamRepository = Depends(get_team_repository),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete teams")

    await repo.delete_team(team_id)
    return {"detail": "Team soft-deleted"}

router.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    return {"token": token}