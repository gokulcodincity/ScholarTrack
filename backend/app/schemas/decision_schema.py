from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict

from app.utils.enums import DecisionStatus


class DecisionCreate(BaseModel):
    """
    Admin records the final decision
    for an application.
    """

    application_id: int

    decision_status: DecisionStatus

    decided_by: int | None = None


class DecisionResponse(BaseModel):
    """
    Decision details returned to client.
    """

    id: int

    application_id: int

    decision_status: DecisionStatus

    decided_by: int

    decided_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class DecisionUpdate(BaseModel):
    """
    Admin can update an existing decision.
    """

    decision_status: DecisionStatus


class DecisionListResponse(BaseModel):
    """
    Used when returning multiple decisions.
    """

    id: int

    application_id: int

    decision_status: DecisionStatus

    decided_by: int

    decided_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )