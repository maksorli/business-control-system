from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_session
from app.schemas.meeting import MeetingCreate, MeetingUpdate, MeetingRead
from app.repositories.meeting_repository import MeetingRepository
from app.kafka.kafka_producer import send_meeting_created_event
from app.utils.validate_calendar import validate_participant_availability

router = APIRouter(prefix="/meetings", tags=["Meetings"])


@router.post("/", response_model=MeetingRead, status_code=status.HTTP_201_CREATED)
async def create_meeting(
    data: MeetingCreate,
    session: AsyncSession = Depends(get_session)
):
 
    for user_id in data.participant_ids:
        is_available = await validate_participant_availability(
            user_id=user_id,
            start_time=data.start_time,
            end_time=data.end_time
        )
        if not is_available:
            raise HTTPException(
                status_code=400,
                detail=f"User {user_id} is busy during this time"
            )

    repo = MeetingRepository(session)
    meeting = await repo.create(data)


    await send_meeting_created_event(
        meeting_id=meeting.id,
        team_id=meeting.team_id,
        start_time=meeting.start_time,
        end_time=meeting.end_time,
        participant_ids=data.participant_ids,
    )
    return meeting


@router.get("/{meeting_id}", response_model=MeetingRead)
async def get_meeting(
    meeting_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    repo = MeetingRepository(session)
    meeting = await repo.get_by_id(meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


@router.patch("/{meeting_id}", response_model=MeetingRead)
async def update_meeting(
    meeting_id: UUID,
    data: MeetingUpdate,
    session: AsyncSession = Depends(get_session)
):
    repo = MeetingRepository(session)
    meeting = await repo.update(meeting_id, data)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


@router.delete("/{meeting_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meeting(
    meeting_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    repo = MeetingRepository(session)
    deleted = await repo.delete(meeting_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Meeting not found")
