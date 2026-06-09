import pytest
from pydantic import ValidationError

from playitloud.repositories import AddressRepository, UserRepository
from playitloud.schemas import AddressCreate, UserCreate
from playitloud.services import AddressService, UserService


def _make_user(db_session):
    user_repo = UserRepository(db_session)
    user_service = UserService(session=db_session, user_repository=user_repo)
    return user_service.create_user(
        UserCreate(
            email="user@test.com",
            password="secret123456",
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

    # blank/whitespace-only fields are rejected (422), not stored
    with pytest.raises(ValidationError):
        AddressCreate(street="   ", city="Paris", postal_code="75001", country_code="FR")


def test_create_address_normalizes_country_code(db_session):
    user = _make_user(db_session)
    service = _make_service(db_session)

    address = service.create_address(
        user.id,
        AddressCreate(street="1 Rue A", city="Paris", postal_code="75001", country_code="fr"),
    )

    assert address.country_code == "FR"


def test_get_address_wrong_user(db_session):
    user = _make_user(db_session)
    service = _make_service(db_session)

    created = service.create_address(
        user.id,
        AddressCreate(street="1 Rue A", city="Paris", postal_code="75001", country_code="FR"),
    )

    with pytest.raises(ValueError, match="Address not found"):
        service.get_address(user_id=9999, address_id=created.id)
