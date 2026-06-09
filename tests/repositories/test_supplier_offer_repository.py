from decimal import Decimal

from playitloud.models import Album, Supplier, SupplierOffer
from playitloud.models.album import MediaType
from playitloud.repositories import SupplierOfferRepository


def _make_supplier(db_session, name: str = "Acme Records") -> Supplier:
    supplier = Supplier(name=name, contact_email=None)
    db_session.add(supplier)
    db_session.commit()
    db_session.refresh(supplier)
    return supplier


def _make_album(db_session, name: str = "Test Album") -> Album:
    album = Album(name=name, media_type=MediaType.CD, price=Decimal("14.99"), stock=10)
    db_session.add(album)
    db_session.commit()
    db_session.refresh(album)
    return album


def _make_offer(db_session, supplier_id: int, album_id: int, price: str = "6.50") -> SupplierOffer:
    offer = SupplierOffer(supplier_id=supplier_id, album_id=album_id, unit_price=Decimal(price))
    db_session.add(offer)
    db_session.commit()
    return offer


def test_add_and_get_by_supplier_and_album(db_session):
    repository = SupplierOfferRepository(db_session)
    supplier = _make_supplier(db_session)
    album = _make_album(db_session)

    _make_offer(db_session, supplier.id, album.id, price="6.50")

    found = repository.get_by_supplier_and_album(supplier.id, album.id)

    assert found is not None
    assert found.unit_price == Decimal("6.50")


def test_get_all_by_supplier_id(db_session):
    repository = SupplierOfferRepository(db_session)
    supplier = _make_supplier(db_session)
    other = _make_supplier(db_session, name="Other Label")
    album_a = _make_album(db_session, name="Album A")
    album_b = _make_album(db_session, name="Album B")

    _make_offer(db_session, supplier.id, album_a.id)
    _make_offer(db_session, supplier.id, album_b.id)
    _make_offer(db_session, other.id, album_a.id)

    offers = repository.get_all_by_supplier_id(supplier.id)

    assert len(offers) == 2
    assert all(o.supplier_id == supplier.id for o in offers)


def test_delete(db_session):
    repository = SupplierOfferRepository(db_session)
    supplier = _make_supplier(db_session)
    album = _make_album(db_session)

    offer = _make_offer(db_session, supplier.id, album.id)

    repository.delete(offer)
    db_session.commit()

    assert repository.get_by_supplier_and_album(supplier.id, album.id) is None
