import os
import shutil

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
    BackgroundTasks,
    Request,
)
from jose import jwt, JWTError
from app.services.email_service import send_verification_email, SECRET_KEY, ALGORITHM

from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.rate_limiter import limiter

from app.schemas.auth_schema import RegisterSchema, LoginSchema

from app.schemas.reviewer_request_schema import ReviewerRequestResponse

from app.services.auth_service import register_user, login_user

from app.models.reviewer_request import ReviewerRequest
from app.repositories.user_repository import UserRepository

RESUME_UPLOAD_DIR = "uploads/resumes"
os.makedirs(RESUME_UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
@limiter.limit("5/minute")
def register(
    request: Request,
    data: RegisterSchema,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    if data.role.upper() not in ["STUDENT", "REVIEWER"]:
        raise HTTPException(
            status_code=403, 
            detail="Public registration is restricted to STUDENT and REVIEWER roles only"
        )

    user = register_user(data, db)

    if not user:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Send verification email in background
    background_tasks.add_task(send_verification_email, user.email, user.name)

    return {
        "message": (
            "Registration successful! Please check your email to verify your account."
        ),
        "user_id": user.id,
        "role": user.role,
    }


@router.post("/reviewer-request", response_model=ReviewerRequestResponse)
def submit_reviewer_request(
    user_id: int = Form(...),
    university: str = Form(...),
    department: str = Form(...),
    years_of_experience: int = Form(...),
    institution_email: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Validate user exists and is PENDING_REVIEWER
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role != "PENDING_REVIEWER":
        raise HTTPException(
            status_code=400,
            detail="Only PENDING_REVIEWER users can submit this request",
        )

    # Check for duplicate submission
    existing = (
        db.query(ReviewerRequest).filter(ReviewerRequest.user_id == user_id).first()
    )
    if existing:
        raise HTTPException(
            status_code=400, detail="Reviewer request already submitted"
        )

    # Validate file type (PDF only)
    if not resume.filename or not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF resumes are accepted")

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
        status="PENDING",
    )

    db.add(request)
    try:
        db.commit()
        db.refresh(request)
    except Exception:
        db.rollback()
        raise

    return request


@router.post("/login")
@limiter.limit("10/minute")
def login(request: Request, data: LoginSchema, db: Session = Depends(get_db)):
    token = login_user(data, db)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if token == "UNVERIFIED_EMAIL":
        raise HTTPException(
            status_code=403,
            detail="Please verify your email to log in. Check your inbox.",
        )

    # Pending reviewer - not yet approved by admin
    if token == "PENDING_APPROVAL":
        raise HTTPException(
            status_code=403,
            detail="Your reviewer request is pending admin approval. Please wait.",
        )

    return {"access_token": token, "token_type": "bearer"}


@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(
            status_code=400, detail="Invalid or expired verification token"
        )

    user_repo = UserRepository(db)
    user = user_repo.get_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.verified_email:
        return {"message": "Email is already verified"}

    user.verified_email = True
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return {"message": "Email verified successfully"}
