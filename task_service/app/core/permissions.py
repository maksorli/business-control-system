from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user
from app.schemas.current_user import CurrentUser

async def require_admin_user(current_user: CurrentUser = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: admin role required"
        )
    return current_user
