from app.models.essay import Essay


async def create_essay(
    application_id: int,
    essay_text: str,
    supporting_content: str | None = None
):

    essay = Essay(
        application_id=application_id,
        essay=essay_text,
        supporting_content=supporting_content
    )

    await essay.insert()

    return essay


async def get_essay(
    application_id: int
):

    return await Essay.find_one(
        Essay.application_id == application_id
    )