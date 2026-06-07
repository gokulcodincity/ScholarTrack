from sqlalchemy.orm import Session
from sqlalchemy import func
 
from app.models.student import Student
from app.models.application import Application
 
 
def create_student(data, db: Session):
 
    student = Student(
        user_id=data.user_id,
        department=data.department,
        cgpa=data.cgpa,
        academic_year=data.academic_year
    )
 
    db.add(student)
    try:
        db.commit()
        db.refresh(student)
    except Exception:
        db.rollback()
        raise
 
    return student
 
 
def get_student_by_id(
    student_id: int,
    db: Session
):
 
    student = db.query(Student).filter(
        Student.user_id == student_id
    ).first()
 
    if not student:
        return None
 
    application_count = (
        db.query(
            func.count(Application.id)
        )
        .filter(
            Application.student_id == student_id
        )
        .scalar()
    )
 
    return {
        "id": student.id,
        "user_id": student.user_id,
        "department": student.department,
        "cgpa": student.cgpa,
        "academic_year": student.academic_year,
        "application_count": application_count
    }