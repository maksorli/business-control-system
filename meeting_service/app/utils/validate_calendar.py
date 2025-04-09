import httpx
from datetime import datetime
from uuid import UUID

CALENDAR_SERVICE_URL = "http://calendar_service:8000"

async def validate_participant_availability(
    user_id: UUID,
    start_time: datetime,
    end_time: datetime
) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{CALENDAR_SERVICE_URL}/calendar/validate",
            json={
                "user_id": str(user_id),
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat()
            }
        )
        if response.status_code == 200:
            return response.json().get("available", False)
        return False
