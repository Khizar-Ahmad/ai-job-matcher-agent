from pydantic import BaseModel


class JobProcessingSchema(BaseModel):
    company_name: str
    job_title: str
    job_description: str
    requirements: str


class QuestionAnswerSchema(BaseModel):
    questions: list[str]