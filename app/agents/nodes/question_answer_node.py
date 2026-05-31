from langchain_core.messages import HumanMessage

from app.services.llm_service import model


async def question_answer_node(state):
    questions = state.get("questions", [])

    answers = []

    for question in questions:
        prompt = f"""
        Answer the following job application question professionally.

        Question:
        {question}

        User Profile:
        {state['user_profile']}

        Resume:
        {state['resume_text'][:4000]}
        """

        response = await model.ainvoke([
            HumanMessage(content=prompt)
        ])

        answers.append({
            "question": question,
            "answer": response.content
        })

    state["application_answers"] = answers

    return state