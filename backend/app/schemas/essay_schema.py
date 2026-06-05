from pydantic import BaseModel


class EssayCreate(BaseModel):

    application_id: int

    essay: str


class EssayResponse(BaseModel):

    id: str

    application_id: int

    essay: str