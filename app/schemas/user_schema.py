from pydantic import BaseModel
from pydantic import EmailStr


class UserResponseSchema(BaseModel):

    id: int

    name: str

    email: EmailStr

    desired_job_title: str

    job_preferences: str

    skills: str

    experience_level: str

    class Config:
        from_attributes = True