from pydantic import BaseModel, EmailStr


class RegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

    desired_job_title: str
    job_preferences: str
    skills: str
    experience_level: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class InternalUserResponse(BaseModel):
    id:                 int
    name:               str
    email:              str
    desired_job_title:  str
    skills:             str
    job_preferences:    str
    experience_level:   str
    class Config:
        from_attributes = True

class Data(BaseModel):
    access_token: str
    user: InternalUserResponse

class SignUpLoginResponse(BaseModel):
    message:str
    data: Data