from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.config.database import get_db

from app.middleware.auth_middleware import (
    require_student
)

from app.schemas.student_schema import (
    StudentCreateSchema
)

from app.services.student_service import (
    create_student,
    get_student_by_id
)

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.post("/")
def create_student_route(
    data: StudentCreateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(require_student)
):
    """
    Create student profile.
    Student token required.
    """

    return create_student(
        data,
        db
    )


@router.get("/{student_id}")
def get_student_route(
    student_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_student)
):
    """
    Get student profile.
    Student token required.
    """

    student = get_student_by_id(
        student_id,
        db
    )

    if not student:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student