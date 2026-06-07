from sqlalchemy.orm import Session
from app.models.student import Student

class StudentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, student: Student) -> Student:
        self.db.add(student)
        try:
            self.db.commit()
            self.db.refresh(student)
        except Exception:
            self.db.rollback()
            raise
        return student
