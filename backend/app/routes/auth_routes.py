import os
import shutil

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form

from sqlalchemy.orm import Session

from app.config.database import get_db

from app.schemas.auth_schema import (
    RegisterSchema,
    LoginSchema
)

from app.schemas.reviewer_request_schema import ReviewerRequestResponse

from app.services.auth_service import (
    register_user,
    login_user
)

from app.models.reviewer_request import ReviewerRequest
from app.models.user import User

RESUME_UPLOAD_DIR = "uploads/resumes"
os.makedirs(RESUME_UPLOAD_DIR, exist_ok=True)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    data: RegisterSchema,
    db: Session = Depends(get_db)
):
    if data.role.upper() == "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Cannot self-register as ADMIN"
        )

    user = register_user(data, db)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return {
        "message": "User registered successfully",
        "user_id": user.id,
        "role": user.role
    }


@router.post("/reviewer-request", response_model=ReviewerRequestResponse)
async def submit_reviewer_request(
    user_id: int = Form(...),
    university: str = Form(...),
    department: str = Form(...),
    years_of_experience: int = Form(...),
    institution_email: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate user exists and is PENDING_REVIEWER
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role != "PENDING_REVIEWER":
        raise HTTPException(
            status_code=400,
            detail="Only PENDING_REVIEWER users can submit this request"
        )

    # Check for duplicate submission
    existing = db.query(ReviewerRequest).filter(
        ReviewerRequest.user_id == user_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Reviewer request already submitted"
        )

    # Validate file type (PDF only)
    if not resume.filename or not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are accepted"
        )

    # Save the resume file
    safe_filename = f"{user_id}_{resume.filename}"
    file_path = os.path.join(RESUME_UPLOAD_DIR, safe_filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    # Save request to DB
    request = ReviewerRequest(
        user_id=user_id,
        university=university,
        department=department,
        years_of_experience=years_of_experience,
        institution_email=institution_email,
        resume_filename=safe_filename,
        status="PENDING"
    )

    db.add(request)
    db.commit()
    db.refresh(request)

    return request


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

    # Pending reviewer - not yet approved by admin
    if token == "PENDING_APPROVAL":
        raise HTTPException(
            status_code=403,
            detail="Your reviewer request is pending admin approval. Please wait."
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }