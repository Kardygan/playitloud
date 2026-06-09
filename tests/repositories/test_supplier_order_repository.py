from decimal import Decimal

from playitloud.models import Album, Supplier, SupplierOrder, SupplierOrderItem
from playitloud.models.album import MediaType
from playitloud.models.supplier_order import RestockStatus
from playitloud.repositories import SupplierOrderRepository


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


def _make_supplier_order(db_session, supplier: Supplier, album: Album) -> SupplierOrder:
    supplier_order = SupplierOrder(
        supplier_id=supplier.id,
        status=RestockStatus.PENDING,
        total_price=Decimal("13.00"),
    )
    supplier_order.supplier_order_items = [
        SupplierOrderItem(album_id=album.id, quantity=2, unit_price=Decimal("6.50")),
    ]
    db_session.add(supplier_order)
    db_session.commit()
    db_session.refresh(supplier_order)
    return supplier_order


def test_add_and_get_by_id_and_supplier_id(db_session):
    repository = SupplierOrderRepository(db_session)
    supplier = _make_supplier(db_session)
    album = _make_album(db_session)

    supplier_order = _make_supplier_order(db_session, supplier, album)

    found = repository.get_by_id_and_supplier_id(supplier_order.id, supplier.id)

    assert found is not None
    assert found.total_price == Decimal("13.00")
    assert len(found.supplier_order_items) == 1
    assert found.supplier_order_items[0].album_id == album.id


def test_get_all_by_supplier_id(db_session):
    repository = SupplierOrderRepository(db_session)
    supplier = _make_supplier(db_session)
    other = _make_supplier(db_session, name="Other Label")
    album = _make_album(db_session)

    _make_supplier_order(db_session, supplier, album)
    _make_supplier_order(db_session, supplier, album)
    _make_supplier_order(db_session, other, album)

    supplier_orders = repository.get_all_by_supplier_id(supplier.id)

    assert len(supplier_orders) == 2
    assert all(o.supplier_id == supplier.id for o in supplier_orders)


def test_delete(db_session):
    repository = SupplierOrderRepository(db_session)
    supplier = _make_supplier(db_session)
    album = _make_album(db_session)

    supplier_order = _make_supplier_order(db_session, supplier, album)
    supplier_order_id = supplier_order.id

    repository.delete(supplier_order)
    db_session.commit()

    assert repository.get_by_id_and_supplier_id(supplier_order_id, supplier.id) is None
