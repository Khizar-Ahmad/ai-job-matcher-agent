from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


class AuthService:

    @staticmethod
    async def register_user(db: AsyncSession, payload):

        existing_user = await UserRepository.get_user_by_email(
            db,
            payload.email
        )

        if existing_user:
            raise Exception("Email already exists")

        hashed_password = hash_password(payload.password)

        user = await UserRepository.create_user(
            db,
            {
                "name": payload.name,
                "email": payload.email,
                "password": hashed_password,
                "desired_job_title": payload.desired_job_title,
                "job_preferences": payload.job_preferences,
                "skills": payload.skills,
                "experience_level": payload.experience_level,
            }
        )

        access_token = create_access_token(
            {"sub": str(user.id)}
        )

        return {
            "access_token": access_token,
            "user": user
        }


    @staticmethod
    async def login_user(db: AsyncSession, payload):

        user = await UserRepository.get_user_by_email(
            db,
            payload.email
        )

        if not user:
            raise Exception("Invalid credentials")

        valid_password = verify_password(
            payload.password,
            user.password
        )

        if not valid_password:
            raise Exception("Invalid credentials")

        access_token = create_access_token(
             {"sub": str(user.id)}
        )

        return {
            "access_token": access_token,
            "user": user
        }