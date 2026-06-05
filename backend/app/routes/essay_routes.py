from fastapi import APIRouter, Depends

from app.middleware.auth_middleware import (
    get_current_user,
    require_student
)

from app.schemas.essay_schema import (
    EssayCreate
)

from app.services.essay_service import (
    create_essay,
    get_essay
)

router = APIRouter(
    prefix="/essays",
    tags=["Essays"]
)


@router.post("/")
async def add_essay(
    essay_data: EssayCreate,
    current_user: dict = Depends(require_student)
):

    return await create_essay(
        essay_data.application_id,
        essay_data.essay,
        essay_data.supporting_content
    )


@router.get("/{application_id}")
async def fetch_essay(
    application_id: int,
    current_user: dict = Depends(get_current_user)
):

    return await get_essay(
        application_id
    )