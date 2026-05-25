from playitloud.models import User
from playitloud.repositories import UserRepository

def test_add_user(db_session):
    repository = UserRepository(db_session)

    user = User(
        email="test@test.com",
        hashed_password="hashed_password",
        first_name="Tommy",
        last_name="Test",
    )

    repository.add(user)
    db_session.commit()
    db_session.refresh(user)

    saved_user = repository.get_by_email("test@test.com")

    assert saved_user is not None
    assert saved_user.email == "test@test.com"

def test_get_user_by_id(db_session):
    repository = UserRepository(db_session)

    user = User(
        email="john@test.com",
        hashed_password="password",
        first_name="John",
        last_name="Doe",
    )

    repository.add(user)
    db_session.commit()
    db_session.refresh(user)

    found_user = repository.get_by_id(user.id)

    assert found_user is not None
    assert found_user.id == user.id
    
def test_get_user_by_email(db_session):
    repository = UserRepository(db_session)

    user = User(
        email="jane@test.com",
        hashed_password="password",
        first_name="Jane",
        last_name="Doe",
    )

    repository.add(user)
    db_session.commit()
    db_session.refresh(user)

    found_user = repository.get_by_email(user.email)

    assert found_user is not None
    assert found_user.email == user.email

def test_get_all_users(db_session):
    repository = UserRepository(db_session)

    user_1 = User(
        email="user1@test.com",
        hashed_password="password",
        first_name="User",
        last_name="One",
    )

    user_2 = User(
        email="user2@test.com",
        hashed_password="password",
        first_name="User",
        last_name="Two",
    )

    repository.add(user_1)
    repository.add(user_2)
    db_session.commit()

    users = repository.get_all()

    assert len(users) == 2

def test_soft_delete_user(db_session):
    repository = UserRepository(db_session)

    user = User(
        email="delete@test.com",
        hashed_password="password",
        first_name="Delete",
        last_name="Me",
    )

    repository.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    repository.soft_delete(user)
    db_session.commit()

    deleted_user = repository.get_by_id(user.id)
    
    assert deleted_user is None