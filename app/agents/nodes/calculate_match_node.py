from app.utils.similarity import calculate_similarity,infer_missing_skills


async def calculate_match_node(state):
    # percentage = await calculate_similarity(
    #     state["resume_skills"],
    #     state["job_skills"]
    # )

    # state["match_percentage"] = percentage

    # return state
    resume_skills = state["resume_skills"]
    job_skills = state["job_skills"]

    # Pass 2 — infer any job skills the candidate implicitly has
    inferred_skills = await infer_missing_skills(resume_skills, job_skills)

    # Merge inferred skills into resume skills before comparison
    enriched_resume_skills = sorted(set(resume_skills + inferred_skills))

    percentage = await calculate_similarity(
        enriched_resume_skills,
        job_skills,
    )

    state["resume_skills"] = enriched_resume_skills
    # state["inferred_skills"] = inferred_skills
    state["match_percentage"] = percentage

    return state