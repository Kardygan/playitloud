from sqlalchemy import select
from sqlalchemy.orm import Session

from playitloud.models import Supplier


class SupplierRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, supplier: Supplier) -> None:
        self.session.add(supplier)

    def get_by_id(self, supplier_id: int) -> Supplier | None:
        statement = select(Supplier).where(Supplier.id == supplier_id)

        return self.session.scalar(statement)

    def get_all(self) -> list[Supplier]:
        statement = select(Supplier)

        return list(self.session.scalars(statement).all())

    def name_exists(self, name: str) -> bool:
        statement = select(Supplier.id).where(Supplier.name == name)

        return self.session.scalar(statement) is not None

    def delete(self, supplier: Supplier) -> None:
        self.session.delete(supplier)
