from langchain_core.tools import tool

from app.utils.similarity import extract_skills


@tool
async def extract_resume_skills_tool(
    resume_text: str
):
    """Extract skills from resume text."""

    skills = await extract_skills(resume_text)

    return {
        "skills": skills
    }