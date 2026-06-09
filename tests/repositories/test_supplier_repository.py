from playitloud.models import Supplier
from playitloud.repositories import SupplierRepository


def _make_supplier(db_session, name: str = "Acme Records") -> Supplier:
    supplier = Supplier(name=name, contact_email="contact@acme.test")
    db_session.add(supplier)
    db_session.commit()
    db_session.refresh(supplier)
    return supplier


def test_add_and_get_by_id(db_session):
    repository = SupplierRepository(db_session)

    supplier = _make_supplier(db_session)

    found = repository.get_by_id(supplier.id)

    assert found is not None
    assert found.name == "Acme Records"


def test_name_exists(db_session):
    repository = SupplierRepository(db_session)

    _make_supplier(db_session, name="Acme Records")

    assert repository.name_exists("Acme Records") is True
    assert repository.name_exists("Other Label") is False


def test_delete(db_session):
    repository = SupplierRepository(db_session)

    supplier = _make_supplier(db_session)
    supplier_id = supplier.id

    repository.delete(supplier)
    db_session.commit()

    assert repository.get_by_id(supplier_id) is None
