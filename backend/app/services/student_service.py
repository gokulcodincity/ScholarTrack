from sqlalchemy.orm import Session

from app.models.student import Student


def create_student(data, db: Session):

    student = Student(
        user_id=data.user_id,
        department=data.department,
        cgpa=data.cgpa,
        academic_year=data.academic_year
    )

    db.add(student)

    db.commit()

    db.refresh(student)

    return student


def get_student_by_id(
    student_id: int,
    db: Session
):

    return db.query(Student).filter(
        Student.id == student_id
    ).first()