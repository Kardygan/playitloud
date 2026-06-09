from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from playitloud.models import SupplierOrder


class SupplierOrderRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, supplier_order: SupplierOrder) -> None:
        self.session.add(supplier_order)

    def get_by_id_and_supplier_id(
        self, supplier_order_id: int, supplier_id: int
    ) -> SupplierOrder | None:
        statement = (
            select(SupplierOrder)
            .where(
                SupplierOrder.id == supplier_order_id,
                SupplierOrder.supplier_id == supplier_id,
            )
            .options(selectinload(SupplierOrder.supplier_order_items))
        )

        return self.session.scalar(statement)

    def get_all_by_supplier_id(self, supplier_id: int) -> list[SupplierOrder]:
        statement = (
            select(SupplierOrder)
            .where(SupplierOrder.supplier_id == supplier_id)
            .options(selectinload(SupplierOrder.supplier_order_items))
        )

        return list(self.session.scalars(statement).all())

    def delete(self, supplier_order: SupplierOrder) -> None:
        self.session.delete(supplier_order)
