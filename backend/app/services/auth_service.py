from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.student_repository import StudentRepository

from app.config.security import (
    hash_password,
    verify_password,
    create_access_token
)


def register_user(data, db: Session):

    user_repo = UserRepository(db)
    existing_user = user_repo.get_by_email(data.email)

    if existing_user:
        return None

    user_role = data.role.upper()
    if user_role == "REVIEWER":
        user_role = "PENDING_REVIEWER"

    user = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        role=user_role
    )

    user = user_repo.create(user)

    # Automatically create an empty Student profile if the user is a STUDENT
    if user.role == "STUDENT":
        from app.models.student import Student
        student_profile = Student(
            user_id=user.id,
            department=data.department,
            cgpa=data.cgpa,
            academic_year=data.academic_year
        )
        student_repo = StudentRepository(db)
        student_repo.create(student_profile)

    return user


def login_user(data, db: Session):

    user_repo = UserRepository(db)
    user = user_repo.get_by_email(data.email)

    if not user:
        return None

    if not verify_password(
        data.password,
        user.password
    ):

        return None

    if not user.verified_email:
        return "UNVERIFIED_EMAIL"

    # Block login until admin approves
    if user.role == "PENDING_REVIEWER":
        return "PENDING_APPROVAL"

    token = create_access_token(
        {
            "id": user.id,
            "role": user.role
        }
    )

    return token