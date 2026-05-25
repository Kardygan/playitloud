from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from playitloud.core.database import SessionLocal
from playitloud.repositories import UserRepository
from playitloud.services import UserService


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_service(session: Session = Depends(get_db)) -> UserService:
    repository = UserRepository(session)
    return UserService(session=session, user_repository=repository)
