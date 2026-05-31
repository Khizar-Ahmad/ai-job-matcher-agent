from fastapi import APIRouter
from fastapi import Depends

from app.dependencies.auth_dependency import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me")
async def get_my_profile(
    current_user = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "desired_job_title": current_user.desired_job_title,
        "job_preferences": current_user.job_preferences,
        "skills": current_user.skills,
        "experience_level": current_user.experience_level,
    }