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

from app.utils.enums import DecisionStatus


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

    db.commit()

    db.refresh(scholarship)

    return scholarship


def get_all_scholarships(
    db: Session,
    field: str | None = None,
    min_amount: float | None = None,
    deadline_before: date | None = None
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

    return query.all()


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
    total_applied = (
        db.query(Application)
        .filter(
            Application.scholarship_id == scholarship_id
        )
        .count()
    )

    decision_counts = (
        db.query(
            Decision.decision_status,
            func.count(Decision.id)
        )
        .join(
            Application,
            Application.id == Decision.application_id
        )
        .filter(
            Application.scholarship_id == scholarship_id
        )
        .group_by(
            Decision.decision_status
        )
        .all()
    )

    awarded = 0
    shortlisted = 0

    for status, count in decision_counts:

        if status == DecisionStatus.APPROVED:
            awarded = count

        elif status == DecisionStatus.WAITLISTED:
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

    db.commit()

    db.refresh(scholarship)

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