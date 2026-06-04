from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.config.database import get_db

from app.middleware.auth_middleware import (
    get_current_user
)

from app.schemas.user_schema import (
    UserResponseSchema
)

from app.services.user_service import (
    get_user_by_id,
    get_all_users
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/",
    response_model=list[UserResponseSchema]
)
def get_users(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Get all users.
    Login required.
    """

    return get_all_users(db)


@router.get(
    "/{user_id}",
    response_model=UserResponseSchema
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Get user by ID.
    Login required.
    """

    user = get_user_by_id(
        user_id,
        db
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user