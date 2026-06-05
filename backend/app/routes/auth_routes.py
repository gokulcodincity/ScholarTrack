from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.config.database import get_db

from app.schemas.auth_schema import (
    RegisterSchema,
    LoginSchema
)

from app.services.auth_service import (
    register_user,
    login_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register")
def register(
    data: RegisterSchema,
    db: Session = Depends(get_db)
):

    user = register_user(data, db)

    if not user:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return {
        "message": "User registered successfully"
    }


@router.post("/login")
def login(
    data: LoginSchema,
    db: Session = Depends(get_db)
):

    token = login_user(data, db)

    if not token:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }