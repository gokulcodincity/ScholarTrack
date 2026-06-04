from sqlalchemy.orm import Session

from app.models.scholarship import Scholarship
from app.schemas.scholarship_schema import (
    ScholarshipCreate,
    ScholarshipUpdate
)


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
    db: Session
):
    return db.query(
        Scholarship
    ).all()


def get_scholarship_by_id(
    db: Session,
    scholarship_id: int
):
    return db.query(
        Scholarship
    ).filter(
        Scholarship.id == scholarship_id
    ).first()


def update_scholarship(
    db: Session,
    scholarship_id: int,
    scholarship_data: ScholarshipUpdate
):
    scholarship = db.query(
        Scholarship
    ).filter(
        Scholarship.id == scholarship_id
    ).first()

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
    scholarship = db.query(
        Scholarship
    ).filter(
        Scholarship.id == scholarship_id
    ).first()

    if not scholarship:
        return False

    db.delete(scholarship)
    db.commit()

    return True