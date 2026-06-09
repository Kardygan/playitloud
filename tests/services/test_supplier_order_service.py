from decimal import Decimal

import pytest

from playitloud.models.album import MediaType
from playitloud.models.supplier_order import RestockStatus
from playitloud.repositories import (
    AlbumRepository,
    ArtistRepository,
    SupplierOfferRepository,
    SupplierOrderRepository,
    SupplierRepository,
)
from playitloud.schemas.album import AlbumCreate
from playitloud.schemas.supplier import SupplierCreate
from playitloud.schemas.supplier_offer import SupplierOfferCreate
from playitloud.schemas.supplier_order import (
    RestockStatusUpdate,
    SupplierOrderCreate,
    SupplierOrderItemCreate,
)
from playitloud.services import (
    AlbumService,
    SupplierOfferService,
    SupplierOrderService,
    SupplierService,
)


def _make_service(db_session) -> SupplierOrderService:
    return SupplierOrderService(
        session=db_session,
        supplier_order_repository=SupplierOrderRepository(db_session),
        supplier_repository=SupplierRepository(db_session),
        album_repository=AlbumRepository(db_session),
        supplier_offer_repository=SupplierOfferRepository(db_session),
    )


def _make_supplier(db_session, name: str = "Acme Records"):
    service = SupplierService(session=db_session, supplier_repository=SupplierRepository(db_session))
    return service.create_supplier(SupplierCreate(name=name))


def _make_album(db_session, stock: int = 10):
    service = AlbumService(
        session=db_session,
        album_repository=AlbumRepository(db_session),
        artist_repository=ArtistRepository(db_session),
    )
    return service.create_album(
        AlbumCreate(name="Test Album", media_type=MediaType.CD, price=Decimal("14.99"), stock=stock)
    )


def _make_offer(db_session, supplier_id: int, album_id: int, price: str = "6.50"):
    service = SupplierOfferService(
        session=db_session,
        supplier_offer_repository=SupplierOfferRepository(db_session),
        supplier_repository=SupplierRepository(db_session),
        album_repository=AlbumRepository(db_session),
    )
    return service.create_offer(
        supplier_id, SupplierOfferCreate(album_id=album_id, unit_price=Decimal(price))
    )


def test_create_supplier_order_snapshots_offer_price(db_session):
    service = _make_service(db_session)
    supplier = _make_supplier(db_session)
    album = _make_album(db_session)
    _make_offer(db_session, supplier.id, album.id, price="6.50")

    supplier_order = service.create_supplier_order(
        supplier.id,
        SupplierOrderCreate(items=[SupplierOrderItemCreate(album_id=album.id, quantity=5)]),
    )

    assert supplier_order.status == RestockStatus.PENDING
    assert supplier_order.total_price == Decimal("32.50")
    assert supplier_order.supplier_order_items[0].unit_price == Decimal("6.50")


def test_create_supplier_order_missing_offer(db_session):
    service = _make_service(db_session)
    supplier = _make_supplier(db_session)
    album = _make_album(db_session)

    with pytest.raises(ValueError, match="Supplier offer for album"):
        service.create_supplier_order(
            supplier.id,
            SupplierOrderCreate(items=[SupplierOrderItemCreate(album_id=album.id, quantity=5)]),
        )


def test_received_increments_stock_once(db_session):
    service = _make_service(db_session)
    album_repository = AlbumRepository(db_session)
    supplier = _make_supplier(db_session)
    album = _make_album(db_session, stock=10)
    _make_offer(db_session, supplier.id, album.id)

    created = service.create_supplier_order(
        supplier.id,
        SupplierOrderCreate(items=[SupplierOrderItemCreate(album_id=album.id, quantity=5)]),
    )

    service.update_supplier_order_status(
        supplier.id, created.id, RestockStatusUpdate(status=RestockStatus.RECEIVED)
    )

    assert album_repository.get_by_id(album.id).stock == 15

    # A repeated PATCH to RECEIVED must not increment stock again.
    service.update_supplier_order_status(
        supplier.id, created.id, RestockStatusUpdate(status=RestockStatus.RECEIVED)
    )

    assert album_repository.get_by_id(album.id).stock == 15
