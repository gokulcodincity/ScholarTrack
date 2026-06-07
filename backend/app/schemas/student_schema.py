from pydantic import BaseModel, ConfigDict
from app.utils.sanitization import SanitizedStr


class StudentCreateSchema(BaseModel):

    user_id: int
    department: SanitizedStr
    cgpa: float
    academic_year: SanitizedStr


class StudentResponseSchema(BaseModel):

    id: int
    user_id: int
    department: str
    cgpa: float
    academic_year: str
    application_count: int

    model_config = ConfigDict(
        from_attributes=True
    )