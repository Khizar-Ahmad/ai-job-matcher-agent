from langchain_core.messages import HumanMessage

from app.services.llm_service import model
from app.utils.prompts import COVER_LETTER_PROMPT
from app.utils.token_manager import trim_text


class CoverLetterService:

    @staticmethod
    async def generate_cover_letter(
        user_profile: dict,
        resume_text: str,
        company_name: str,
        job_title: str,
        job_description: str,
    ):

        cleaned_resume = await trim_text(
            resume_text,
            4000
        )

        cleaned_job_description = await trim_text(
            job_description,
            3000
        )

        prompt = COVER_LETTER_PROMPT.format(
            user_profile=user_profile,
            resume_text=cleaned_resume,
            company_name=company_name,
            job_title=job_title,
            job_description=cleaned_job_description,
        )

        response = await model.ainvoke([
            HumanMessage(content=prompt)
        ])

        return response.content