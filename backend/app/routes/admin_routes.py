from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.config.database import get_db

from app.middleware.auth_middleware import (
    require_admin
)

from app.schemas.decision_schema import (
    DecisionCreate,
    DecisionUpdate,
    DecisionResponse
)

from app.services.decision_service import (
    create_decision,
    get_decision_by_id,
    get_application_decision,
    get_all_decisions,
    update_decision,
    delete_decision
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.post(
    "/decisions",
    response_model=DecisionResponse
)
def create_new_decision(
    decision_data: DecisionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Admin records final decision.
    """

    decision = create_decision(
        db,
        decision_data
    )

    if not decision:
        raise HTTPException(
            status_code=400,
            detail=(
                "Decision cannot be created. "
                "Review may not be completed or "
                "decision already exists."
            )
        )

    return decision


@router.get(
    "/decisions",
    response_model=list[DecisionResponse]
)
def get_decisions(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Get all decisions.
    """

    return get_all_decisions(db)


@router.get(
    "/decisions/{decision_id}",
    response_model=DecisionResponse
)
def get_decision(
    decision_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Get decision by ID.
    """

    decision = get_decision_by_id(
        db,
        decision_id
    )

    if not decision:
        raise HTTPException(
            status_code=404,
            detail="Decision not found"
        )

    return decision


@router.get(
    "/applications/{application_id}/decision",
    response_model=DecisionResponse
)
def get_decision_for_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Get decision for a specific application.
    """

    decision = get_application_decision(
        db,
        application_id
    )

    if not decision:
        raise HTTPException(
            status_code=404,
            detail="Decision not found"
        )

    return decision


@router.patch(
    "/decisions/{decision_id}",
    response_model=DecisionResponse
)
def update_existing_decision(
    decision_id: int,
    decision_data: DecisionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Update decision status.
    """

    decision = update_decision(
        db,
        decision_id,
        decision_data
    )

    if not decision:
        raise HTTPException(
            status_code=404,
            detail="Decision not found"
        )

    return decision


@router.delete(
    "/decisions/{decision_id}"
)
def remove_decision(
    decision_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Delete decision.
    """

    deleted = delete_decision(
        db,
        decision_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Decision not found"
        )

    return {
        "message": "Decision deleted successfully"
    }