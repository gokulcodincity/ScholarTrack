from pydantic import BaseModel, ConfigDict
from typing import Optional


class ReviewerRequestResponse(BaseModel):
    id: int
    user_id: int
    university: str
    department: str
    years_of_experience: int
    institution_email: str
    resume_filename: Optional[str] = None
    status: str

    model_config = ConfigDict(from_attributes=True)
