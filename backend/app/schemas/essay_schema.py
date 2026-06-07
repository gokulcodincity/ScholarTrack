from pydantic import BaseModel
from app.utils.sanitization import SanitizedStr
from beanie import PydanticObjectId


class EssayCreate(BaseModel):

    application_id: int

    essay: SanitizedStr

    supporting_content: SanitizedStr | None = None


class EssayResponse(BaseModel):

    id: PydanticObjectId

    application_id: int

    essay: str

    supporting_content: str | None = None