import os
import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends, HTTPException,Request
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies.auth_dependency import get_current_user
from app.utils.file_parser import parse_resume
# from app.agents.graph import job_graph
# from app.main import job_graph
from app.services.resume_service import ResumeService

from app.services.question_service import QuestionService
from langgraph.types import Command


router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/process")
async def process_job_application(
    request: Request,
    company_name: str = Form(...),
    job_title: str = Form(...),
    job_description: str = Form(...),
    requirements: str = Form(...),
    resume: UploadFile = File(...),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    thread_id = f"user_{current_user.id}_{uuid.uuid4()}"
    config = {"configurable": {"thread_id": thread_id}}
    resume_text = await ResumeService.upload_and_extract_text(
        resume
    )
    print(f"Thread Id: {thread_id}")

    # file_extension = resume.filename.split(".")[-1]

    # unique_name = f"{uuid.uuid4()}.{file_extension}"

    # file_path = f"uploads/{unique_name}"

    # with open(file_path, "wb") as file:
    #     content = await resume.read()
    #     file.write(content)

    # resume_text = await parse_resume(file_path)
    job_graph = request.app.state.job_graph
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

    result = await job_graph.ainvoke(state,config=config)

    # os.remove(file_path)

    return {
        "match_percentage": result["match_percentage"],
        "resume_skills": result["resume_skills"],
        "job_skills": result["job_skills"],
        # "cover_letter": result["cover_letter"],
        "thread_id": thread_id, 
    }

@router.post("/resume/{thread_id}")
async def resume_job_application(
    request:Request,
    thread_id: str,
    feedback: str = Form(""),
    finalize: bool = Form(False),
    current_user=Depends(get_current_user)
):
    config = {"configurable": {"thread_id": thread_id}}
    job_graph = request.app.state.job_graph

    await job_graph.aupdate_state(
        config,
        {"human_feedback": feedback, "regenerate_decision": "done" if finalize else "continue"}
    )
    print("Before call")
    result = await job_graph.ainvoke(
        # Command(resume={"feedback": feedback}),
        None,
        config=config
    )
    print("After call")

    
    if result.get("error"):
        raise HTTPException(status_code=500, detail=result["error"])
    if result["cover_letter"] == "__skipped__":
        return {
            "cover_letter": None,
            "message": "Cover letter generation was skipped per your feedback."
        }
    
    return {"cover_letter": result["cover_letter"]}


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