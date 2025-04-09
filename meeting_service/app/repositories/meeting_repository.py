from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from uuid import UUID
from app.models.meeting import Meeting, MeetingParticipant
from app.schemas.meeting import MeetingCreate, MeetingUpdate
from datetime import datetime

class MeetingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: MeetingCreate) -> Meeting:
        meeting = Meeting(
            title=data.title,
            description=data.description,
            start_time=data.start_time,
            end_time=data.end_time,
            team_id=data.team_id,
            organizer_id=data.organizer_id
        )
        self.session.add(meeting)
        await self.session.flush()   

        for user_id in data.participant_ids:
            self.session.add(MeetingParticipant(meeting_id=meeting.id, user_id=user_id))

        await self.session.commit()
        await self.session.refresh(meeting)
        return meeting

    async def get_by_id(self, meeting_id: UUID) -> Meeting | None:
        result = await self.session.execute(select(Meeting).where(Meeting.id == meeting_id))
        return result.scalar_one_or_none()

    async def update(self, meeting_id: UUID, data: MeetingUpdate) -> Meeting | None:
        meeting = await self.get_by_id(meeting_id)
        if not meeting:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            if field != "participant_ids":
                setattr(meeting, field, value)

        if data.participant_ids is not None:
            await self.session.execute(delete(MeetingParticipant).where(MeetingParticipant.meeting_id == meeting_id))
            for user_id in data.participant_ids:
                self.session.add(MeetingParticipant(meeting_id=meeting_id, user_id=user_id))

        await self.session.commit()
        await self.session.refresh(meeting)
        return meeting

    async def delete(self, meeting_id: UUID) -> bool:
        result = await self.session.execute(delete(Meeting).where(Meeting.id == meeting_id))
        await self.session.commit()
        return result.rowcount > 0
