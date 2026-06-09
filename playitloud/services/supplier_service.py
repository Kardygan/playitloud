from sqlalchemy.orm import Session

from playitloud.models import Supplier
from playitloud.repositories.supplier_repository import SupplierRepository
from playitloud.schemas.supplier import SupplierCreate, SupplierRead, SupplierUpdate


class SupplierService:
    def __init__(self, session: Session, supplier_repository: SupplierRepository) -> None:
        self.session = session
        self.supplier_repository = supplier_repository

    def create_supplier(self, supplier_create: SupplierCreate) -> SupplierRead:
        if self.supplier_repository.name_exists(supplier_create.name):
            raise ValueError(f'Supplier "{supplier_create.name}" already exists.')

        supplier = Supplier(
            name=supplier_create.name,
            contact_email=supplier_create.contact_email,
        )

        self.supplier_repository.add(supplier)
        self.session.commit()
        self.session.refresh(supplier)

        return SupplierRead.model_validate(supplier)

    def get_supplier_by_id(self, supplier_id: int) -> SupplierRead:
        supplier = self.supplier_repository.get_by_id(supplier_id)

        if not supplier:
            raise ValueError(f"Supplier with id {supplier_id} not found.")

        return SupplierRead.model_validate(supplier)

    def get_all_suppliers(self) -> list[SupplierRead]:
        return [SupplierRead.model_validate(s) for s in self.supplier_repository.get_all()]

    def update_supplier(self, supplier_id: int, supplier_update: SupplierUpdate) -> SupplierRead:
        supplier = self.supplier_repository.get_by_id(supplier_id)

        if not supplier:
            raise ValueError(f"Supplier with id {supplier_id} not found.")

        if supplier_update.name != supplier.name and self.supplier_repository.name_exists(
            supplier_update.name
        ):
            raise ValueError(f'Supplier "{supplier_update.name}" already exists.')

        supplier.name = supplier_update.name
        supplier.contact_email = supplier_update.contact_email

        self.session.commit()
        self.session.refresh(supplier)

        return SupplierRead.model_validate(supplier)

    def delete_supplier(self, supplier_id: int) -> None:
        supplier = self.supplier_repository.get_by_id(supplier_id)

        if not supplier:
            raise ValueError(f"Supplier with id {supplier_id} not found.")

        self.supplier_repository.delete(supplier)
        self.session.commit()
