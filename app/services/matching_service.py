from app.utils.similarity import (
    extract_skills,
    calculate_similarity
)


class MatchingService:

    @staticmethod
    async def calculate_job_match(
        resume_text: str,
        job_description: str,
        requirements: str
    ):

        combined_job_text = (
            job_description + " " + requirements
        )

        resume_skills = await extract_skills(
            resume_text
        )

        job_skills = await extract_skills(
            combined_job_text
        )

        similarity_percentage = await calculate_similarity(
            resume_skills,
            job_skills
        )

        missing_skills = list(
            set(job_skills) - set(resume_skills)
        )

        matched_skills = list(
            set(job_skills).intersection(set(resume_skills))
        )

        return {
            "resume_skills": resume_skills,
            "job_skills": job_skills,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "similarity_percentage": similarity_percentage
        }