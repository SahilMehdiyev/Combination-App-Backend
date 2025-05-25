from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from combination_app.config.database import get_db
from combination_app.schemas.auth import Token, LoginRequest
from combination_app.schemas.user import UserCreate, UserResponse
from combination_app.services.auth_service import AuthService
from combination_app.utils.helpers import create_response


router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=dict)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        auth_service = AuthService(db)
        user = auth_service.create_user(user_data)

        return create_response(
            success=True,
            message="User successfully registered.",
            data={
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "full_name": user.full_name,
                }
            },
        )

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration.",
        )


@router.post("/login", response_model=dict)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(login_data.username, login_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password wrong",
        )

    token = auth_service.create_access_token_for_user(user)

    return create_response(
        success=True,
        message="Login successful",
        data={
            "access_token": token.access_token,
            "token_type": token.token_type,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
            },
        },
    )
