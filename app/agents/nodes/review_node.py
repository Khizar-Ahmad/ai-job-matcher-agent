
from langgraph.types import interrupt

async def review_node(state):
    human_feedback = interrupt({
        "match_percentage": state["match_percentage"],
        "resume_skills": state["resume_skills"],
        "job_skills": state["job_skills"],
        "message": "Paused before cover letter generation"
    })
    state["human_feedback"] = human_feedback.get("feedback", "")
    return state

