import pytest

from playitloud.repositories import UserRepository
from playitloud.schemas import UserCreate, UserUpdateInfo
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
    
def test_login_user_invalid_email(db_session):
    repository = UserRepository(db_session)

    service = UserService(
        session=db_session,
        user_repository=repository,
    )

    with pytest.raises(ValueError):
        service.login_user(
            email="unknown@test.com",
            password="secret123",
        )
        
def test_login_user_invalid_password(db_session):
    repository = UserRepository(db_session)

    service = UserService(
        session=db_session,
        user_repository=repository,
    )

    service.create_user(
        UserCreate(
            email="login@test.com",
            password="correct_password",
            first_name="Tommy",
            last_name="Test",
        )
    )

    with pytest.raises(ValueError):
        service.login_user(
            email="login@test.com",
            password="wrong_password",
        )

def test_get_user_by_id(db_session):
    repository = UserRepository(db_session)

    service = UserService(
        session=db_session,
        user_repository=repository,
    )

    created_user = service.create_user(
        UserCreate(
            email="find@test.com",
            password="password",
            first_name="Find",
            last_name="Me",
        )
    )

    found_user = service.get_user_by_id(created_user.id)

    assert found_user.id == created_user.id
    
def test_get_user_by_email(db_session):
    repository = UserRepository(db_session)

    service = UserService(
        session=db_session,
        user_repository=repository,
    )

    service.create_user(
        UserCreate(
            email="email@test.com",
            password="password",
            first_name="Email",
            last_name="Test",
        )
    )

    found_user = service.get_user_by_email("email@test.com")

    assert found_user.email == "email@test.com"
    
def test_update_user_info(db_session):
    repository = UserRepository(db_session)

    service = UserService(
        session=db_session,
        user_repository=repository,
    )

    created_user = service.create_user(
        UserCreate(
            email="update@test.com",
            password="password",
            first_name="Old",
            last_name="Name",
        )
    )

    updated_user = service.update_user_info(
        created_user.id,
        UserUpdateInfo(
            first_name="New",
            last_name="Name",
        ),
    )

    assert updated_user.first_name == "New"
    
def test_delete_user(db_session):
    repository = UserRepository(db_session)

    service = UserService(
        session=db_session,
        user_repository=repository,
    )

    created_user = service.create_user(
        UserCreate(
            email="delete@test.com",
            password="password",
            first_name="Delete",
            last_name="Me",
        )
    )

    service.delete_user(created_user.id)
    deleted_user = repository.get_by_id(created_user.id)

    assert deleted_user is None