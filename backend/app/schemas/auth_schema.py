from pydantic import BaseModel, EmailStr


class RegisterSchema(BaseModel):

    name: str

    email: EmailStr

    password: str

    role: str

    department: str | None = None

    cgpa: float | None = None

    academic_year: str | None = None


class LoginSchema(BaseModel):

    email: EmailStr

    password: str