from beanie import Document


class Essay(Document):

    application_id: int

    essay: str

    class Settings:
        name = "essays"