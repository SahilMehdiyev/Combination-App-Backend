from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from config.database import get_db
from schemas.user import UserResponse, UserUpdate
from services.user_service import UserService
from api.dependencies import get_current_active_user, get_current_superuser
from models.user import User
from utils.helpers import create_response


router = APIRouter(prefix='/users', tags =['users'])

@router.get('/me', response_model=dict)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
): 
    return create_response(
        success=True,
        message="User info",
        data={
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "is_verified": current_user.is_verified,
            "created_at": current_user.created_at,
            "updated_at": current_user.updated_at
        }
    )
    
    
@router.put("/me", response_model=dict)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    updated_user = user_service.update_user(current_user.id, user_data, current_user)
    
    return create_response(
        success=True,
        message="User information updated",
        data={
            "id": updated_user.id,
            "username": updated_user.username,
            "email": updated_user.email,
            "full_name": updated_user.full_name,
            "is_verified": updated_user.is_verified,
            "updated_at": updated_user.updated_at
        }
    )

@router.get("/{user_id}", response_model=dict)
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return create_response(
        success=True,
        message="User info",
        data={
            "id": user.id,
            "username": user.username,
            "email": user.email if user.id == current_user.id or current_user.is_superuser else None,
            "full_name": user.full_name,
            "created_at": user.created_at
        }
    )

@router.get("/", response_model=dict)
async def get_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    user_service = UserService(db)
    users = user_service.get_users(page, per_page)
    
    return create_response(
        success=True,
        message="Users list",
        data={
            "users": [
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "full_name": user.full_name,
                    "is_verified": user.is_verified,
                    "is_superuser": user.is_superuser,
                    "created_at": user.created_at
                }
                for user in users
            ],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": len(users)
            }
        }
    )