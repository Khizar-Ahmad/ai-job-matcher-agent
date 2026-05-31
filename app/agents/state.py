from typing import TypedDict


class AgentState(TypedDict):
    user_profile: dict

    resume_text: str

    company_name: str
    job_title: str
    job_description: str
    requirements: str

    resume_skills: list[str]
    job_skills: list[str]

    match_percentage: float

    cover_letter: str

    application_answers: list