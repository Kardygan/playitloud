from playitloud.models import Address, User
from playitloud.repositories import AddressRepository


def _make_user(db_session) -> User:
    user = User(
        email="user@test.com",
        hashed_password="hashed",
        first_name="Test",
        last_name="User",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def test_add_address(db_session):
    user = _make_user(db_session)
    repository = AddressRepository(db_session)

    address = Address(
        user_id=user.id,
        street="123 Main St",
        city="Paris",
        postal_code="75001",
        country_code="FR",
    )

    repository.add(address)
    db_session.commit()
    db_session.refresh(address)

    found = repository.get_by_id_and_user_id(address.id, user.id)

    assert found is not None
    assert found.street == "123 Main St"
    assert found.user_id == user.id


def test_get_by_id_and_user_id_wrong_user(db_session):
    user = _make_user(db_session)
    repository = AddressRepository(db_session)

    address = Address(
        user_id=user.id,
        street="123 Main St",
        city="Paris",
        postal_code="75001",
        country_code="FR",
    )

    repository.add(address)
    db_session.commit()
    db_session.refresh(address)

    found = repository.get_by_id_and_user_id(address.id, user_id=9999)

    assert found is None


def test_get_all_by_user_id(db_session):
    user = _make_user(db_session)
    repository = AddressRepository(db_session)

    other_user = User(
        email="other@test.com",
        hashed_password="hashed",
        first_name="Other",
        last_name="User",
    )
    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    repository.add(Address(user_id=user.id, street="1 Rue A", city="Lyon", postal_code="69001", country_code="FR"))
    repository.add(Address(user_id=user.id, street="2 Rue B", city="Lyon", postal_code="69002", country_code="FR"))
    repository.add(Address(user_id=other_user.id, street="3 Rue C", city="Nice", postal_code="06000", country_code="FR"))
    db_session.commit()

    addresses = repository.get_all_by_user_id(user.id)

    assert len(addresses) == 2
    assert all(a.user_id == user.id for a in addresses)


def test_delete_address(db_session):
    user = _make_user(db_session)
    repository = AddressRepository(db_session)

    address = Address(
        user_id=user.id,
        street="123 Main St",
        city="Paris",
        postal_code="75001",
        country_code="FR",
    )

    repository.add(address)
    db_session.commit()
    db_session.refresh(address)

    address_id = address.id
    repository.delete(address)
    db_session.commit()

    found = repository.get_by_id_and_user_id(address_id, user.id)

    assert found is None
