from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from combination_app.config.database import get_db
from combination_app.schemas.combination import (
    CombinationCreate,
    CombinationUpdate,
    CombinationResponse,
)
from combination_app.services.combination_service import CombinationService
from combination_app.api.dependencies import get_current_active_user
from combination_app.models.user import User
from combination_app.utils.helpers import create_response


router = APIRouter(prefix="/combinations", tags=["combinations"])


@router.post("/", response_model=dict)
async def create_combinations(
    combination_data: CombinationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    combination_service = CombinationService(db)
    combination = combination_service.create_combination(combination_data, current_user)

    return create_response(
        success=True,
        message="Combination create successfully",
        data={
            "id": combination.id,
            "title": combination.title,
            "description": combination.description,
            "items": combination.items,
            "category": combination.category,
            "tags": combination.tags,
            "owner_id": combination.owner_id,
            "created_at": combination.created_at,
        },
    )


@router.get("/", response_model=dict)
async def get_combinations(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    owner_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    combination_service = CombinationService(db)
    combinations = combination_service.get_combinations(
        page=page,
        per_page=per_page,
        category=category,
        search=search,
        owner_id=owner_id,
    )

    return create_response(
        success=True,
        message="Combination List",
        data={
            "combinations": [
                {
                    "id": combo.id,
                    "title": combo.title,
                    "description": combo.description,
                    "items": combo.items,
                    "category": combo.category,
                    "tags": combo.tags,
                    "owner_id": combo.owner_id,
                    "created_at": combo.created_at,
                    "updated_at": combo.updated_at,
                }
                for combo in combinations
            ],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": len(combinations),
            },
        },
    )


@router.get("/my", response_model=dict)
async def get_my_combinations(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    combination_service = CombinationService(db)
    combinations = combination_service.get_user_combinations(
        user_id=current_user.id, page=page, per_page=per_page
    )

    return create_response(
        success=True,
        message="Get Your combinations",
        data={
            "combinations": [
                {
                    "id": combo.id,
                    "title": combo.title,
                    "description": combo.description,
                    "items": combo.items,
                    "category": combo.category,
                    "tags": combo.tags,
                    "created_at": combo.created_at,
                    "updated_at": combo.updated_at,
                }
                for combo in combinations
            ],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": len(combinations),
            },
        },
    )


@router.get("/{combination_id}", response_model=dict)
async def get_combination(
    combination_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    combination_service = CombinationService(db)
    combination = combination_service.get_combination_by_id(combination_id)

    if not combination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Combination not found"
        )

    return create_response(
        success=True,
        message="Combination information list",
        data={
            "id": combination.id,
            "title": combination.title,
            "description": combination.description,
            "items": combination.items,
            "category": combination.category,
            "tags": combination.tags,
            "owner_id": combination.owner_id,
            "created_at": combination.created_at,
            "updated_at": combination.updated_at,
        },
    )


@router.put("/{combination_id}", response_model=dict)
async def update_combination(
    combination_id: int,
    combination_data: CombinationUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    combination_service = CombinationService(db)
    combination = combination_service.update_combination(
        combination_id, combination_data, current_user
    )

    return create_response(
        success=True,
        message="Combination update",
        data={
            "id": combination.id,
            "title": combination.title,
            "description": combination.description,
            "items": combination.items,
            "category": combination.category,
            "tags": combination.tags,
            "updated_at": combination.updated_at,
        },
    )


@router.delete("/{combination_id}", response_model=dict)
async def delete_combination(
    combination_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    combination_service = CombinationService(db)
    success = combination_service.delete_combination(combination_id, current_user)

    if success:
        return create_response(success=True, message="Combination deleted")
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Combination not delete",
        )
