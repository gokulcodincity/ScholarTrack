from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.config.database import get_db

from app.services.user_service import (
    get_user_by_id,
    get_all_users
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/")
def get_users(
    db: Session = Depends(get_db)
):

    return get_all_users(db)


@router.get("/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = get_user_by_id(user_id, db)

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user