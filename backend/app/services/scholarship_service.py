from datetime import date

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.scholarship import Scholarship
from app.models.application import Application
from app.models.decision import Decision

from app.schemas.scholarship_schema import (
    ScholarshipCreate,
    ScholarshipUpdate
)

from app.utils.enums import DecisionStatus, ApplicationStatus


def create_scholarship(
    db: Session,
    scholarship_data: ScholarshipCreate
):
    scholarship = Scholarship(
        title=scholarship_data.title,
        field=scholarship_data.field,
        amount=scholarship_data.amount,
        eligibility=scholarship_data.eligibility,
        deadline=scholarship_data.deadline
    )

    db.add(scholarship)

    try:
        db.commit()
        db.refresh(scholarship)
    except Exception:
        db.rollback()
        raise

    return scholarship


def get_all_scholarships(
    db: Session,
    field: str | None = None,
    min_amount: float | None = None,
    deadline_before: date | None = None,
    skip: int = 0,
    limit: int = 100
):
    query = db.query(Scholarship)

    if field:
        query = query.filter(
            Scholarship.field.ilike(f"%{field}%")
        )

    if min_amount:
        query = query.filter(
            Scholarship.amount >= min_amount
        )

    if deadline_before:
        query = query.filter(
            Scholarship.deadline <= deadline_before
        )

    return query.offset(skip).limit(limit).all()


def get_scholarship_by_id(
    db: Session,
    scholarship_id: int
):
    return (
        db.query(Scholarship)
        .filter(
            Scholarship.id == scholarship_id
        )
        .first()
    )


from sqlalchemy import func

def get_scholarship_stats(
    db: Session,
    scholarship_id: int
):
    rows = (
        db.query(
            Application.status,
            func.count(Application.id)
        )
        .filter(
            Application.scholarship_id == scholarship_id
        )
        .group_by(
            Application.status
        )
        .all()
    )

    total_applied = 0
    awarded = 0
    shortlisted = 0

    for status, count in rows:
        total_applied += count
        
        if status == ApplicationStatus.AWARDED:
            awarded = count
        elif status == ApplicationStatus.SHORTLISTED:
            shortlisted = count

    return {
        "scholarship_id": scholarship_id,
        "total_applied": total_applied,
        "shortlisted": shortlisted,
        "awarded": awarded
    }
def update_scholarship(
    db: Session,
    scholarship_id: int,
    scholarship_data: ScholarshipUpdate
):
    scholarship = (
        db.query(Scholarship)
        .filter(
            Scholarship.id == scholarship_id
        )
        .first()
    )

    if not scholarship:
        return None

    update_data = scholarship_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            scholarship,
            key,
            value
        )

    try:
        db.commit()
        db.refresh(scholarship)
    except Exception:
        db.rollback()
        raise

    return scholarship


def delete_scholarship(
    db: Session,
    scholarship_id: int
):
    scholarship = (
        db.query(Scholarship)
        .filter(
            Scholarship.id == scholarship_id
        )
        .first()
    )

    if not scholarship:
        return False

    db.delete(scholarship)

    db.commit()

    return True