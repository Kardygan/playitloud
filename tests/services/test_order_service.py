import pytest
from decimal import Decimal

from playitloud.models.album import MediaType
from playitloud.models.order import OrderStatus
from playitloud.repositories import (
    AddressRepository,
    AlbumRepository,
    ArtistRepository,
    OrderRepository,
    UserRepository,
)
from playitloud.schemas import AddressCreate, UserCreate
from playitloud.schemas.album import AlbumCreate
from playitloud.schemas.order import OrderCreate, OrderItemCreate, OrderStatusUpdate
from playitloud.services import AddressService, AlbumService, OrderService, UserService


def _make_order_service(db_session) -> OrderService:
    return OrderService(
        session=db_session,
        order_repository=OrderRepository(db_session),
        user_repository=UserRepository(db_session),
        address_repository=AddressRepository(db_session),
        album_repository=AlbumRepository(db_session),
    )


def _make_user(db_session):
    user_service = UserService(session=db_session, user_repository=UserRepository(db_session))
    return user_service.create_user(
        UserCreate(
            email="user@test.com",
            password="secret123456",
            first_name="Test",
            last_name="User",
        )
    )


def _make_address(db_session, user_id: int):
    address_service = AddressService(
        session=db_session,
        address_repository=AddressRepository(db_session),
        user_repository=UserRepository(db_session),
    )
    return address_service.create_address(
        user_id,
        AddressCreate(street="1 Rue A", city="Paris", postal_code="75001", country_code="FR"),
    )


def _make_album(db_session, price: str = "14.99", stock: int = 10):
    album_service = AlbumService(
        session=db_session,
        album_repository=AlbumRepository(db_session),
        artist_repository=ArtistRepository(db_session),
    )
    return album_service.create_album(
        AlbumCreate(name="Test Album", media_type=MediaType.CD, price=Decimal(price), stock=stock)
    )


def test_create_order_snapshots_price_and_decrements_stock(db_session):
    service = _make_order_service(db_session)
    album_repository = AlbumRepository(db_session)

    user = _make_user(db_session)
    address = _make_address(db_session, user.id)
    album = _make_album(db_session, price="14.99", stock=10)

    order = service.create_order(
        user.id,
        OrderCreate(address_id=address.id, items=[OrderItemCreate(album_id=album.id, quantity=2)]),
    )

    assert order.status == OrderStatus.PENDING
    assert order.total_price == Decimal("29.98")
    assert order.order_items[0].unit_price == Decimal("14.99")
    updated_album = album_repository.get_by_id(album.id)
    assert updated_album is not None
    assert updated_album.stock == 8


def test_create_order_insufficient_stock(db_session):
    service = _make_order_service(db_session)

    user = _make_user(db_session)
    address = _make_address(db_session, user.id)
    album = _make_album(db_session, stock=1)

    with pytest.raises(ValueError, match="Insufficient stock"):
        service.create_order(
            user.id,
            OrderCreate(address_id=address.id, items=[OrderItemCreate(album_id=album.id, quantity=5)]),
        )


def test_update_order_status(db_session):
    service = _make_order_service(db_session)

    user = _make_user(db_session)
    address = _make_address(db_session, user.id)
    album = _make_album(db_session)

    created = service.create_order(
        user.id,
        OrderCreate(address_id=address.id, items=[OrderItemCreate(album_id=album.id, quantity=1)]),
    )

    updated = service.update_order_status(
        user.id, created.id, OrderStatusUpdate(status=OrderStatus.PAID)
    )

    assert updated.id == created.id
    assert updated.status == OrderStatus.PAID
