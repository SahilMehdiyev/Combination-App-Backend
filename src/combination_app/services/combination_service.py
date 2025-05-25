from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.combination import Combination
from models.user import User
from schemas.combination import CombinationCreate, CombinationUpdate
from utils.helpers import paginate_query


class CombinationService:
    def __init__(self, db: Session):
        self.db = db
        
    
    def create_combination(self, combination_data: CombinationCreate, current_user: User) -> Combination:
        db_combination = Combination(
            title = combination_data.title,
            description = combination_data.description,
            items = combination_data.items,
            category = combination_data.category,
            tags = combination_data.tags or [],
            owner_id = current_user.id
        )
        
        self.db.add(db_combination)
        self.db.commit()
        self.db.refresh(db_combination)
        
        return db_combination
    
    
    def get_combination_by_id(self, combination_id: int) -> Optional[Combination]:
        return self.db.query(Combination).filter(
            Combination.id == combination_id,
            Combination.is_active == True
        ).first()
        

    def get_combinations(
        self, 
        page: int = 1, 
        per_page: int = 10,
        owner_id: Optional[int] = None,
        category: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Combination]:
        
        query = self.db.query(Combination).filter(Combination.is_active == True)
        
        if owner_id:
            query = query.filter(Combination.owner_id == owner_id)
            
        if category:
            query = query.filter(Combination.category == category)
            
        if search:
            query = query.filter(
                Combination.title.ilike(f'%{search}%' | 
                Combination.description.ilike(f'%{search}%'))
            )
            
        query = query.order_by(Combination.created_at.desc())
        return paginate_query(query, page, per_page).all()
    
    
        