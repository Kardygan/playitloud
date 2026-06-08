from decimal import Decimal

from playitloud.models import Address, Album, Order, OrderItem, User
from playitloud.models.album import MediaType
from playitloud.models.order import OrderStatus
from playitloud.repositories import OrderRepository


def _make_user(db_session, email: str = "user@test.com") -> User:
    user = User(
        email=email,
        hashed_password="hashed",
        first_name="Test",
        last_name="User",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def _make_address(db_session, user: User) -> Address:
    address = Address(
        user_id=user.id,
        street="123 Main St",
        city="Paris",
        postal_code="75001",
        country_code="FR",
    )
    db_session.add(address)
    db_session.commit()
    db_session.refresh(address)
    return address


def _make_album(db_session, name: str = "Test Album") -> Album:
    album = Album(name=name, media_type=MediaType.CD, price=Decimal("14.99"), stock=10)
    db_session.add(album)
    db_session.commit()
    db_session.refresh(album)
    return album


def _make_order(db_session, user: User, address: Address, album: Album) -> Order:
    order = Order(
        user_id=user.id,
        address_id=address.id,
        status=OrderStatus.PENDING,
        total_price=Decimal("29.98"),
    )
    order.order_items = [
        OrderItem(album_id=album.id, quantity=2, unit_price=Decimal("14.99")),
    ]
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)
    return order


def test_add_and_get_by_id_and_user_id(db_session):
    user = _make_user(db_session)
    address = _make_address(db_session, user)
    album = _make_album(db_session)
    repository = OrderRepository(db_session)

    order = _make_order(db_session, user, address, album)

    found = repository.get_by_id_and_user_id(order.id, user.id)

    assert found is not None
    assert found.user_id == user.id
    assert found.total_price == Decimal("29.98")
    assert len(found.order_items) == 1
    assert found.order_items[0].album_id == album.id


def test_get_all_by_user_id(db_session):
    user = _make_user(db_session)
    address = _make_address(db_session, user)
    album = _make_album(db_session)
    repository = OrderRepository(db_session)

    other_user = _make_user(db_session, email="other@test.com")
    other_address = _make_address(db_session, other_user)

    _make_order(db_session, user, address, album)
    _make_order(db_session, user, address, album)
    _make_order(db_session, other_user, other_address, album)

    orders = repository.get_all_by_user_id(user.id)

    assert len(orders) == 2
    assert all(o.user_id == user.id for o in orders)


def test_delete(db_session):
    user = _make_user(db_session)
    address = _make_address(db_session, user)
    album = _make_album(db_session)
    repository = OrderRepository(db_session)

    order = _make_order(db_session, user, address, album)
    order_id = order.id

    repository.delete(order)
    db_session.commit()

    assert repository.get_by_id_and_user_id(order_id, user.id) is None
