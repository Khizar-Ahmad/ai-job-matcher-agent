import os
import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies.auth_dependency import get_current_user
from app.utils.file_parser import parse_resume
from app.agents.graph import job_graph
from app.services.resume_service import ResumeService

from app.services.question_service import QuestionService

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/process")
async def process_job_application(
    company_name: str = Form(...),
    job_title: str = Form(...),
    job_description: str = Form(...),
    requirements: str = Form(...),
    resume: UploadFile = File(...),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    
    resume_text = await ResumeService.upload_and_extract_text(
        resume
    )

    # file_extension = resume.filename.split(".")[-1]

    # unique_name = f"{uuid.uuid4()}.{file_extension}"

    # file_path = f"uploads/{unique_name}"

    # with open(file_path, "wb") as file:
    #     content = await resume.read()
    #     file.write(content)

    # resume_text = await parse_resume(file_path)

    state = {
        "user_profile": {
            "name": current_user.name,
            "desired_job_title": current_user.desired_job_title,
            "job_preferences": current_user.job_preferences,
            "skills": current_user.skills,
            "experience_level": current_user.experience_level,
        },
        "resume_text": resume_text,
        "company_name": company_name,
        "job_title": job_title,
        "job_description": job_description,
        "requirements": requirements,
    }

    result = await job_graph.ainvoke(state)

    # os.remove(file_path)

    return {
        "match_percentage": result["match_percentage"],
        "resume_skills": result["resume_skills"],
        "job_skills": result["job_skills"],
        "cover_letter": result["cover_letter"],
    }


@router.post("/questions")
async def answer_questions(
    questions: list[str] = Form(...),
    resume: UploadFile = File(...),
    current_user=Depends(get_current_user),
):

    resume_text = await ResumeService.upload_and_extract_text(
        resume
    )

    answers = await QuestionService.answer_application_questions(
        questions=questions,
        user_profile={
            "name": current_user.name,
            "desired_job_title": current_user.desired_job_title,
            "job_preferences": current_user.job_preferences,
            "skills": current_user.skills,
            "experience_level": current_user.experience_level,
        },
        resume_text=resume_text,
    )

    return {
        "success": True,
        "questions_and_answers": answers
    }