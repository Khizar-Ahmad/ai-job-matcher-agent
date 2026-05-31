from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_model import User


class UserRepository:

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str):
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()


    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int):
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()


    @staticmethod
    async def create_user(db: AsyncSession, user_data: dict):
        user = User(**user_data)

        db.add(user)

        await db.commit()
        await db.refresh(user)

        return user