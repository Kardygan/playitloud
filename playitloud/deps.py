from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from playitloud.core.database import SessionLocal
from playitloud.repositories import AddressRepository, UserRepository
from playitloud.services import AddressService, UserService


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_service(session: Session = Depends(get_db)) -> UserService:
    repository = UserRepository(session)
    return UserService(session=session, user_repository=repository)


def get_address_service(session: Session = Depends(get_db)) -> AddressService:
    address_repository = AddressRepository(session)
    user_repository = UserRepository(session)
    return AddressService(
        session=session,
        address_repository=address_repository,
        user_repository=user_repository,
    )
