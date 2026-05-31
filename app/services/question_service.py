# from langchain_core.messages import HumanMessage

# from app.services.llm_service import model
# from app.utils.prompts import QUESTION_ANSWER_PROMPT
# from app.utils.token_manager import trim_text
# from app.services.llm_service import LLMService



# class QuestionService:

#     @staticmethod
#     async def answer_application_questions(
#         questions: list[str],
#         user_profile: dict,
#         resume_text: str,
#     ):

#         cleaned_resume = await trim_text(
#             resume_text,
#             4000
#         )

#         results = []

#         for question in questions:

#             prompt = QUESTION_ANSWER_PROMPT.format(
#                 question=question,
#                 user_profile=user_profile,
#                 resume_text=cleaned_resume,
#             )

#             # response = await model.ainvoke([
#             #     HumanMessage(content=prompt)
#             # ])
#             answer = await LLMService.generate(prompt)

#             results.append({
#                 "question": question,
#                 "answer": answer
#             })

#         return results

import json

from app.utils.prompts import QUESTION_ANSWER_PROMPT
from app.utils.token_manager import trim_text
from app.services.llm_service import LLMService


class QuestionService:

    @staticmethod
    async def answer_application_questions(
        questions: list[str],
        user_profile: dict,
        resume_text: str,
    ):
        cleaned_resume = await trim_text(resume_text, 4000)

        # Format questions as a numbered list for clarity
        formatted_questions = "\n".join(
            f"{i+1}. {q}" for i, q in enumerate(questions)
        )

        prompt = QUESTION_ANSWER_PROMPT.format(
            questions=formatted_questions,
            user_profile=user_profile,
            resume_text=cleaned_resume,
        )

        raw = await LLMService.generate(prompt,"question_answer")

        try:
            # Strip markdown fences if model wraps in ```json ... ```
            clean = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            results = json.loads(clean)
        except json.JSONDecodeError:
            # Graceful fallback: return raw answer under all questions
            results = [
                {"question": q, "answer": raw}
                for q in questions
            ]

        return results