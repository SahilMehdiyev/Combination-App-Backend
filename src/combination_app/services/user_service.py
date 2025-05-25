from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from combination_app.models.user import User
from combination_app.schemas.user import UserUpdate
from combination_app.utils.security import get_password_hash
from combination_app.utils.helpers import paginate_query


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return (
            self.db.query(User)
            .filter(User.id == user_id, User.is_active == True)
            .first()
        )

    def get_user_by_username(self, username: str) -> Optional[User]:
        return (
            self.db.query(User)
            .filter(User.username == username, User.is_active == True)
            .first()
        )

    def get_user_by_email(self, email: str) -> Optional[User]:
        return (
            self.db.query(User)
            .filter(User.email == email, User.is_active == True)
            .first()
        )

    def get_users(self, page: int = 1, per_page: int = 10) -> List[User]:
        query = self.db.query(User).filter(User.is_active == True)
        return paginate_query(query, page, per_page).all()

    def update_user(
        self, user_id: int, user_data: UserUpdate, current_user: User
    ) -> User:
        user = self.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        if user.id != current_user.id and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission for this operation.",
            )

        if user_data.email and user_data.email != user.email:
            existing_user = self.get_user_by_email(user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This email is already in use.",
                )

        if user_data.username and user_data.username != user.username:
            existing_user = self.get_user_by_username(user_data.username)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This username is already in use.",
                )

        for field, value in user_data.dict(exclude_unset=True).items():
            if field == "password" and value:
                setattr(user, "hashed_password", get_password_hash(value))
            elif field != "password":
                setattr(user, field, value)

        self.db.commit()
        self.db.refresh(user)

    def delete_user(self, user_id: int, current_user: User) -> bool:
        user = self.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        if user.id != current_user.id and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You do not have permission for this operation.",
            )

        user.is_active = False
        self.db.commit()

        return True
