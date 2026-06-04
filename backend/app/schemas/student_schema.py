from pydantic import BaseModel


class StudentCreateSchema(BaseModel):

    user_id: int

    department: str

    cgpa: float

    academic_year: str