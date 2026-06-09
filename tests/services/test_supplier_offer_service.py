from decimal import Decimal

import pytest

from playitloud.models.album import MediaType
from playitloud.repositories import (
    AlbumRepository,
    ArtistRepository,
    SupplierOfferRepository,
    SupplierRepository,
)
from playitloud.schemas.album import AlbumCreate
from playitloud.schemas.supplier import SupplierCreate
from playitloud.schemas.supplier_offer import SupplierOfferCreate, SupplierOfferUpdate
from playitloud.services import AlbumService, SupplierOfferService, SupplierService


def _make_service(db_session) -> SupplierOfferService:
    return SupplierOfferService(
        session=db_session,
        supplier_offer_repository=SupplierOfferRepository(db_session),
        supplier_repository=SupplierRepository(db_session),
        album_repository=AlbumRepository(db_session),
    )


def _make_supplier(db_session, name: str = "Acme Records"):
    service = SupplierService(session=db_session, supplier_repository=SupplierRepository(db_session))
    return service.create_supplier(SupplierCreate(name=name))


def _make_album(db_session):
    service = AlbumService(
        session=db_session,
        album_repository=AlbumRepository(db_session),
        artist_repository=ArtistRepository(db_session),
    )
    return service.create_album(
        AlbumCreate(name="Test Album", media_type=MediaType.CD, price=Decimal("14.99"), stock=10)
    )


def test_create_offer(db_session):
    service = _make_service(db_session)
    supplier = _make_supplier(db_session)
    album = _make_album(db_session)

    offer = service.create_offer(
        supplier.id, SupplierOfferCreate(album_id=album.id, unit_price=Decimal("6.50"))
    )

    assert offer.supplier_id == supplier.id
    assert offer.album_id == album.id
    assert offer.unit_price == Decimal("6.50")


def test_create_offer_unknown_album(db_session):
    service = _make_service(db_session)
    supplier = _make_supplier(db_session)

    with pytest.raises(ValueError, match="not found"):
        service.create_offer(
            supplier.id, SupplierOfferCreate(album_id=999, unit_price=Decimal("6.50"))
        )


def test_update_offer(db_session):
    service = _make_service(db_session)
    supplier = _make_supplier(db_session)
    album = _make_album(db_session)

    service.create_offer(
        supplier.id, SupplierOfferCreate(album_id=album.id, unit_price=Decimal("6.50"))
    )

    updated = service.update_offer(
        supplier.id, album.id, SupplierOfferUpdate(unit_price=Decimal("7.25"))
    )

    assert updated.unit_price == Decimal("7.25")
