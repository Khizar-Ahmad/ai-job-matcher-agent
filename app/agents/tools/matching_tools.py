from langchain_core.tools import tool

from app.utils.similarity import calculate_similarity


@tool
async def calculate_similarity_tool(
    resume_skills: list[str],
    job_skills: list[str]
):
    """Calculate job similarity percentage."""

    percentage = await calculate_similarity(
        resume_skills,
        job_skills
    )

    return {
        "match_percentage": percentage
    }