from pydantic import BaseModel, EmailStr, field_validator
from app.utils.sanitization import SanitizedStr


class RegisterSchema(BaseModel):

    name: SanitizedStr

    email: EmailStr

    password: str

    role: SanitizedStr

    department: SanitizedStr | None = None

    cgpa: float | None = None

    academic_year: SanitizedStr | None = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class LoginSchema(BaseModel):

    email: EmailStr

    password: str