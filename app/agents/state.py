from typing import TypedDict


class AgentState(TypedDict):
    user_profile: dict

    resume_text: str
    human_feedback: str   # feedback from user before cover letter
    error: str     
    company_name: str
    job_title: str
    job_description: str
    requirements: str
    regenerate_decision: bool

    resume_skills: list[str]
    job_skills: list[str]

    match_percentage: float

    cover_letter: str

    application_answers: list