from pydantic import BaseModel


class EssayCreate(BaseModel):

    application_id: int

    essay: str

    supporting_content: str | None = None


class EssayResponse(BaseModel):

    id: str

    application_id: int

    essay: str

    supporting_content: str | None = None