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

#     IMPORTANT:
#     - Return ONLY the cover letter text itself.
#     - Do NOT include any preamble like "Here is a cover letter..." or "Sure, here's...".
#     - Do NOT include any closing notes, explanations, or commentary after the letter.
#     - Start directly with "Dear..." and end with the signature.
#     """

#     result = await LLMService.generate(prompt,"cover_letter")

#     state["cover_letter"] = result

#     return state

from app.services.llm_service import LLMService

async def cover_letter_node(state):
    feedback = state.get("human_feedback", "").strip()

    # Explicit skip from the frontend button — no LLM call needed
    if feedback == "__skip__":
        state["cover_letter"] = "__skipped__"
        return state

    # If user typed free-text feedback, ask LLM to classify intent first
    if feedback:
        # intent_prompt = f"""
        # A user gave the following feedback about generating a cover letter:
        # "{feedback}"

        # Does this feedback indicate the user does NOT want a cover letter generated?
        # Respond with exactly one word: "no" if they don't want it, or "yes" if they do want it generated.
        # Do not include any other text.
        # """
        intent_prompt = f"""
        A user was asked if they want a cover letter generated for their job application.
        They responded with the following message:

        "{feedback}"

        Carefully read their message. People often write casually or use words like 
        "blow my mind" to mean they want an excellent cover letter — that is still a YES.

        Only answer "no" if the user explicitly says they do NOT want a cover letter, 
        such as "skip it", "I don't need one", "no thanks", or similar direct refusals.

        If there is ANY ambiguity, or if the message contains instructions, preferences, 
        or context for the cover letter (tone, content, what to emphasize), treat it as "yes".

        Respond with exactly one word: "yes" or "no". Nothing else.
        """
        intent = await LLMService.generate(intent_prompt, "intent_check")
        intent = intent.strip().lower()

        if intent == "no":
            state["cover_letter"] = "__skipped__"
            state["error"] = ""  # not an error, just a clean skip
            return state

    # Otherwise proceed with normal generation
    feedback_block = ""
    if feedback:
        feedback_block = f"""
    User's Specific Instructions for This Cover Letter:
    {feedback}

    Make sure the cover letter reflects these instructions closely.
    """

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
    {feedback_block}

    IMPORTANT:
    - Return ONLY the cover letter text itself.
    - Do NOT include any preamble like "Here is a cover letter..." or "Sure, here's...".
    - Do NOT include any closing notes, explanations, or commentary after the letter.
    - Start directly with "Dear..." and end with the signature.
    """

    result = await LLMService.generate(prompt, "cover_letter")
    state["cover_letter"] = result
    return state