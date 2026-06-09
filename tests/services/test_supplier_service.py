import pytest

from playitloud.repositories import SupplierRepository
from playitloud.schemas.supplier import SupplierCreate, SupplierUpdate
from playitloud.services import SupplierService


def _make_service(db_session) -> SupplierService:
    return SupplierService(session=db_session, supplier_repository=SupplierRepository(db_session))


def test_create_supplier(db_session):
    service = _make_service(db_session)

    supplier = service.create_supplier(
        SupplierCreate(name="Acme Records", contact_email="contact@acme.com")
    )

    assert supplier.id is not None
    assert supplier.name == "Acme Records"
    assert supplier.contact_email == "contact@acme.com"


def test_create_supplier_duplicate_name(db_session):
    service = _make_service(db_session)

    service.create_supplier(SupplierCreate(name="Acme Records"))

    with pytest.raises(ValueError, match="already exists"):
        service.create_supplier(SupplierCreate(name="Acme Records"))


def test_update_supplier(db_session):
    service = _make_service(db_session)

    created = service.create_supplier(SupplierCreate(name="Acme Records"))

    updated = service.update_supplier(
        created.id, SupplierUpdate(name="Acme Vinyl", contact_email="hi@acme.com")
    )

    assert updated.id == created.id
    assert updated.name == "Acme Vinyl"
    assert updated.contact_email == "hi@acme.com"
