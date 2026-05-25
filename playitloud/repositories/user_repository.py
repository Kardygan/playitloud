from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from playitloud.models import User

class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, user: User) -> None:
        self.session.add(user)

    def get_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(
            User.id == user_id, 
            User.deleted_at.is_(None),
        )
        
        return self.session.scalar(statement)

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(
            User.email == email, 
            User.deleted_at.is_(None),
        )
        
        return self.session.scalar(statement)

    def get_all(self) -> list[User]:
        statement = select(User).where(User.deleted_at.is_(None))
        
        return list(self.session.scalars(statement).all())

    def soft_delete(self, user: User) -> None:
        user.deleted_at = datetime.now(UTC)