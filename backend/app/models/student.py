from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey
)

from app.config.database import Base


class Student(Base):

    __tablename__ = "students"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    department = Column(String)

    cgpa = Column(Float)

    academic_year = Column(String)