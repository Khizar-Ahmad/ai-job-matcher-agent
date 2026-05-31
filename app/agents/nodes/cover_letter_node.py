# from langchain_core.messages import HumanMessage

# # from app.services.llm_service import model
# from app.services.llm_service import LLMService

# async def cover_letter_node(state):
#     prompt = f"""
#     Generate a professional cover letter.

#     User Profile:
#     {state['user_profile']}

#     Resume:
#     {state['resume_text'][:5000]}

#     Job Title:
#     {state['job_title']}

#     Company:
#     {state['company_name']}

#     Job Description:
#     {state['job_description'][:4000]}
#     """

#     # response = await model.ainvoke([
#     #     HumanMessage(content=prompt)
#     # ])
#     result = await LLMService.generate(prompt)

#     state["cover_letter"] = result

#     return state

from app.services.llm_service import LLMService

async def cover_letter_node(state):
    prompt = f"""
    Generate a professional cover letter.

    User Profile:
    {state['user_profile']}

    Resume:
    {state['resume_text'][:5000]}

    Job Title:
    {state['job_title']}

    Company:
    {state['company_name']}

    Job Description:
    {state['job_description'][:4000]}

    IMPORTANT:
    - Return ONLY the cover letter text itself.
    - Do NOT include any preamble like "Here is a cover letter..." or "Sure, here's...".
    - Do NOT include any closing notes, explanations, or commentary after the letter.
    - Start directly with "Dear..." and end with the signature.
    """

    result = await LLMService.generate(prompt,"cover_letter")

    state["cover_letter"] = result

    return state