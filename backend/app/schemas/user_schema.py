from pydantic import BaseModel, ConfigDict


class UserResponseSchema(BaseModel):

    id: int
    name: str
    email: str
    role: str

    model_config = ConfigDict(
        from_attributes=True
    )