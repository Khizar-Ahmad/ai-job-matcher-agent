# from app.utils.similarity import extract_skills
from app.utils.similarity import extract_skills_llm


async def parse_resume_node(state):
    skills = await extract_skills_llm(state["resume_text"])

    state["resume_skills"] = skills

    return state