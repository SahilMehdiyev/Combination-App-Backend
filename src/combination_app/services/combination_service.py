from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from combination_app.models.combination import Combination
from combination_app.models.user import User
from combination_app.schemas.combination import CombinationCreate, CombinationUpdate
from combination_app.utils.helpers import paginate_query


class CombinationService:
    def __init__(self, db: Session):
        self.db = db

    def create_combination(
        self, combination_data: CombinationCreate, current_user: User
    ) -> Combination:
        db_combination = Combination(
            title=combination_data.title,
            description=combination_data.description,
            items=combination_data.items,
            category=combination_data.category,
            tags=combination_data.tags or [],
            owner_id=current_user.id,
        )

        self.db.add(db_combination)
        self.db.commit()
        self.db.refresh(db_combination)

        return db_combination

    def get_combination_by_id(self, combination_id: int) -> Optional[Combination]:
        return (
            self.db.query(Combination)
            .filter(Combination.id == combination_id, Combination.is_active == True)
            .first()
        )

    def get_combinations(
        self,
        page: int = 1,
        per_page: int = 10,
        owner_id: Optional[int] = None,
        category: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[Combination]:
        query = self.db.query(Combination).filter(Combination.is_active == True)

        if owner_id:
            query = query.filter(Combination.owner_id == owner_id)

        if category:
            query = query.filter(Combination.category == category)

        if search:
            query = query.filter(
                Combination.title.ilike(
                    f"%{search}%" | Combination.description.ilike(f"%{search}%")
                )
            )

        query = query.order_by(Combination.created_at.desc())
        return paginate_query(query, page, per_page).all()

    def update_combination(
        self,
        combination_id: int,
        combination_data: CombinationUpdate,
        current_user: User,
    ) -> Combination:
        combination = self.get_combination_by_id(combination_id)

        if not combination:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Combination not found"
            )

        if combination.owner_id != current_user.id and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission for this operation.",
            )

        for field, value in combination_data.dict(exclude_unset=True).items():
            setattr(combination, field, value)

        self.db.commit()
        self.db.refresh(combination)

        return combination

    def delete_combination(self, combination_id: int, current_user: User) -> bool:
        combination = self.get_combination_by_id(combination_id)

        if not combination:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Combination not found"
            )

        if combination.owner_id != current_user.id and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission for this operation.",
            )

        combination.is_active = False
        self.db.commit()

        return True

    def get_user_combinations(
        self, user_id: int, page: int = 1, per_page: int = 10
    ) -> List[Combination]:
        query = (
            self.db.query(Combination)
            .filter(Combination.owner_id == user_id, Combination.is_active == True)
            .order_by(Combination.created_at.desc())
        )

        return paginate_query(query, page, per_page).all()
