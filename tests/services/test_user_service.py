import pytest

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
        password="secret123",
        first_name="Tommy",
        last_name="Test",
    )

    created_user = service.create_user(user_create)

    assert created_user.email == "test@test.com"
    assert created_user.first_name == "Tommy"


def test_create_user_duplicate_email(db_session):
    repository = UserRepository(db_session)

    service = UserService(
        session=db_session,
        user_repository=repository,
    )

    user_create = UserCreate(
        email="duplicate@test.com",
        password="secret123",
        first_name="Tommy",
        last_name="Test",
    )

    service.create_user(user_create)

    with pytest.raises(ValueError):
        service.create_user(user_create)


def test_login_user_success(db_session):
    repository = UserRepository(db_session)

    service = UserService(
        session=db_session,
        user_repository=repository,
    )

    service.create_user(
        UserCreate(
            email="login@test.com",
            password="password",
            first_name="Sign",
            last_name="In",
        )
    )

    logged_user = service.login_user("login@test.com", "password")

    assert logged_user
