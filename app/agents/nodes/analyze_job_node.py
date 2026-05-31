from app.utils.similarity import extract_skills_llm


async def analyze_job_node(state):
    job_text = state["job_description"] + "\n" + state["requirements"]

    state["job_skills"] = await extract_skills_llm(job_text)

    return state