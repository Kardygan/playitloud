import pytest
from pydantic import ValidationError

from playitloud.repositories import UserRepository
from playitloud.schemas import UserCreate
from playitloud.services import UserService


def test_create_user(db_session):
    repository = UserRepository(db_session)

    service = UserService(
        session=db_session,
        user_repository=repository,
    )

    user_create = UserCreate(
        email="test@test.com",
        password="secret123456",
        first_name="Tommy",
        last_name="Test",
    )

    created_user = service.create_user(user_create)

    assert created_user.email == "test@test.com"
    assert created_user.first_name == "Tommy"

    # blank names and sub-policy passwords are rejected (422), not stored
    with pytest.raises(ValidationError):
        UserCreate(email="blank@test.com", password="secret123456", first_name="   ", last_name="Test")
    with pytest.raises(ValidationError):
        UserCreate(email="short@test.com", password="short", first_name="Tommy", last_name="Test")


def test_create_user_duplicate_email(db_session):
    repository = UserRepository(db_session)

    service = UserService(
        session=db_session,
        user_repository=repository,
    )

    user_create = UserCreate(
        email="duplicate@test.com",
        password="secret123456",
        first_name="Tommy",
        last_name="Test",
    )

    created = service.create_user(user_create)

    with pytest.raises(ValueError):
        service.create_user(user_create)

    # A soft-deleted user's email stays taken (must not 500 on reuse).
    service.delete_user(created.id)

    with pytest.raises(ValueError):
        service.create_user(user_create)
