from beanie import Document


class Essay(Document):

    application_id: int

    essay: str

    supporting_content: str | None = None

    class Settings:
        name = "essays"