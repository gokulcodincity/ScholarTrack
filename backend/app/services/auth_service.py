from sqlalchemy.orm import Session

from app.models.user import User

from app.config.security import (
    hash_password,
    verify_password,
    create_access_token
)


def register_user(data, db: Session):

    existing_user = db.query(User).filter(
        User.email == data.email
    ).first()

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

    db.add(user)
    db.commit()
    db.refresh(user)

    # Automatically create an empty Student profile if the user is a STUDENT
    if user.role == "STUDENT":
        from app.models.student import Student
        student_profile = Student(
            user_id=user.id,
            department=data.department,
            cgpa=data.cgpa,
            academic_year=data.academic_year
        )
        db.add(student_profile)
        db.commit()

    return user


def login_user(data, db: Session):

    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:

        return None

    if not verify_password(
        data.password,
        user.password
    ):

        return None

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