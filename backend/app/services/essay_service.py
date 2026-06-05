from app.models.essay import Essay


async def create_essay(
    application_id: int,
    essay_text: str
):

    essay = Essay(
        application_id=application_id,
        essay=essay_text
    )

    await essay.insert()

    return essay


async def get_essay(
    application_id: int
):

    return await Essay.find_one(
        Essay.application_id == application_id
    )