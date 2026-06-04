from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.config.database import get_db

from app.schemas.scholarship_schema import (
    ScholarshipCreate,
    ScholarshipUpdate,
    ScholarshipResponse
)

from app.services.scholarship_service import (
    create_scholarship,
    get_all_scholarships,
    get_scholarship_by_id,
    update_scholarship,
    delete_scholarship
)

router = APIRouter(
    prefix="/scholarships",
    tags=["Scholarships"]
)


@router.post(
    "/",
    response_model=ScholarshipResponse
)
def create_new_scholarship(
    scholarship_data: ScholarshipCreate,
    db: Session = Depends(get_db)
):
    return create_scholarship(
        db,
        scholarship_data
    )


@router.get(
    "/",
    response_model=list[ScholarshipResponse]
)
def get_scholarships(
    db: Session = Depends(get_db)
):
    return get_all_scholarships(db)


@router.get(
    "/{scholarship_id}",
    response_model=ScholarshipResponse
)
def get_scholarship(
    scholarship_id: int,
    db: Session = Depends(get_db)
):
    scholarship = get_scholarship_by_id(
        db,
        scholarship_id
    )

    if not scholarship:
        raise HTTPException(
            status_code=404,
            detail="Scholarship not found"
        )

    return scholarship


@router.patch(
    "/{scholarship_id}",
    response_model=ScholarshipResponse
)
def update_existing_scholarship(
    scholarship_id: int,
    scholarship_data: ScholarshipUpdate,
    db: Session = Depends(get_db)
):
    scholarship = update_scholarship(
        db,
        scholarship_id,
        scholarship_data
    )

    if not scholarship:
        raise HTTPException(
            status_code=404,
            detail="Scholarship not found"
        )

    return scholarship


@router.delete(
    "/{scholarship_id}"
)
def remove_scholarship(
    scholarship_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_scholarship(
        db,
        scholarship_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Scholarship not found"
        )

    return {
        "message": "Scholarship deleted successfully"
    }