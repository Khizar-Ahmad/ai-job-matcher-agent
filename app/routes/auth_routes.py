from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.schemas.auth_schema import (
    RegisterSchema,
    LoginSchema,
    SignUpLoginResponse
)

from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=SignUpLoginResponse)
async def register_user(
    payload: RegisterSchema,
    db: AsyncSession = Depends(get_db)
):
    print('end point hit')
    try:
        response = await AuthService.register_user(
            db,
            payload
        )

        return {
            "message": "User registered successfully",
            "data": response
        }

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.post("/login",response_model=SignUpLoginResponse)
async def login_user(
    payload: LoginSchema,
    db: AsyncSession = Depends(get_db)
):

    try:
        response = await AuthService.login_user(
            db,
            payload
        )

        return {
            "message": "Login successful",
            "data": response
        }

    except Exception as error:
        raise HTTPException(
            status_code=401,
            detail=str(error)
        )