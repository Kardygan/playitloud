import pytest

from playitloud.repositories import AddressRepository, UserRepository
from playitloud.schemas import AddressCreate, AddressUpdate, UserCreate
from playitloud.services import AddressService, UserService


def _make_user(db_session):
    user_repo = UserRepository(db_session)
    user_service = UserService(session=db_session, user_repository=user_repo)
    return user_service.create_user(
        UserCreate(
            email="user@test.com",
            password="secret123",
            first_name="Test",
            last_name="User",
        )
    )


def _make_service(db_session) -> AddressService:
    return AddressService(
        session=db_session,
        address_repository=AddressRepository(db_session),
        user_repository=UserRepository(db_session),
    )


def test_create_address(db_session):
    user = _make_user(db_session)
    service = _make_service(db_session)

    address = service.create_address(
        user.id,
        AddressCreate(street="1 Rue A", city="Paris", postal_code="75001", country_code="FR"),
    )

    assert address.id is not None
    assert address.user_id == user.id
    assert address.city == "Paris"


def test_create_address_user_not_found(db_session):
    service = _make_service(db_session)

    with pytest.raises(ValueError, match="User not found"):
        service.create_address(
            9999,
            AddressCreate(street="1 Rue A", city="Paris", postal_code="75001", country_code="FR"),
        )


def test_get_address(db_session):
    user = _make_user(db_session)
    service = _make_service(db_session)

    created = service.create_address(
        user.id,
        AddressCreate(street="1 Rue A", city="Paris", postal_code="75001", country_code="FR"),
    )

    found = service.get_address(user.id, created.id)

    assert found.id == created.id


def test_get_address_not_found(db_session):
    user = _make_user(db_session)
    service = _make_service(db_session)

    with pytest.raises(ValueError, match="Address not found"):
        service.get_address(user.id, 9999)


def test_get_address_wrong_user(db_session):
    user = _make_user(db_session)
    service = _make_service(db_session)

    created = service.create_address(
        user.id,
        AddressCreate(street="1 Rue A", city="Paris", postal_code="75001", country_code="FR"),
    )

    with pytest.raises(ValueError, match="Address not found"):
        service.get_address(user_id=9999, address_id=created.id)


def test_get_user_addresses(db_session):
    user = _make_user(db_session)
    service = _make_service(db_session)

    service.create_address(user.id, AddressCreate(street="1 Rue A", city="Paris", postal_code="75001", country_code="FR"))
    service.create_address(user.id, AddressCreate(street="2 Rue B", city="Lyon", postal_code="69001", country_code="FR"))

    addresses = service.get_user_addresses(user.id)

    assert len(addresses) == 2


def test_update_address(db_session):
    user = _make_user(db_session)
    service = _make_service(db_session)

    created = service.create_address(
        user.id,
        AddressCreate(street="Old Street", city="Paris", postal_code="75001", country_code="FR"),
    )

    updated = service.update_address(
        user.id,
        created.id,
        AddressUpdate(street="New Street", city="Paris", postal_code="75001", country_code="FR"),
    )

    assert updated.street == "New Street"
    assert updated.id == created.id


def test_delete_address(db_session):
    user = _make_user(db_session)
    service = _make_service(db_session)

    created = service.create_address(
        user.id,
        AddressCreate(street="1 Rue A", city="Paris", postal_code="75001", country_code="FR"),
    )

    service.delete_address(user.id, created.id)

    with pytest.raises(ValueError, match="Address not found"):
        service.get_address(user.id, created.id)
