from datetime import date

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.config.database import get_db

from app.middleware.auth_middleware import (
    get_current_user,
    require_admin
)
from app.config.redis import get_cache, set_cache, delete_cache

from app.schemas.scholarship_schema import (
    ScholarshipCreate,
    ScholarshipUpdate,
    ScholarshipResponse,
    ScholarshipStatsResponse
)

from app.services.scholarship_service import (
    create_scholarship,
    get_all_scholarships,
    get_scholarship_by_id,
    get_scholarship_stats,
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
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Admin creates scholarship.
    """

    scholarship = create_scholarship(
        db,
        scholarship_data
    )
    delete_cache("scholarships:*")
    return scholarship


@router.get(
    "/",
    response_model=list[ScholarshipResponse]
)
def get_scholarships(
    skip: int = 0,
    limit: int = 100,
    field: str | None = None,
    min_amount: float | None = None,
    deadline_before: date | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    List scholarships with optional filters.
    """

    cache_key = f"scholarships:{skip}:{limit}:{field}:{min_amount}:{deadline_before}"
    cached_data = get_cache(cache_key)
    if cached_data:
        return cached_data

    scholarships = get_all_scholarships(
        db,
        field,
        min_amount,
        deadline_before,
        skip,
        limit
    )

    data = [
        {
            "id": s.id,
            "title": s.title,
            "amount": float(s.amount),
            "deadline": str(s.deadline),
            "field": s.field,
            "eligibility": s.eligibility
        } for s in scholarships
    ]
    set_cache(cache_key, data, expire_seconds=300)
    return scholarships


@router.get(
    "/{scholarship_id}/stats",
    response_model=ScholarshipStatsResponse
)
def get_scholarship_statistics(
    scholarship_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Get scholarship application statistics.
    """

    scholarship = get_scholarship_by_id(
        db,
        scholarship_id
    )

    if not scholarship:
        raise HTTPException(
            status_code=404,
            detail="Scholarship not found"
        )

    return get_scholarship_stats(
        db,
        scholarship_id
    )


@router.get(
    "/{scholarship_id}",
    response_model=ScholarshipResponse
)
def get_scholarship(
    scholarship_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Get scholarship by ID.
    """

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
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Admin updates scholarship.
    """

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

    delete_cache("scholarships:*")
    return scholarship


@router.delete(
    "/{scholarship_id}"
)
def remove_scholarship(
    scholarship_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Admin deletes scholarship.
    """

    deleted = delete_scholarship(
        db,
        scholarship_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Scholarship not found"
        )

    delete_cache("scholarships:*")
    return {
        "message": "Scholarship deleted successfully"
    }