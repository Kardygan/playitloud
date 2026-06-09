from sqlalchemy.orm import Session

from playitloud.models import SupplierOrder, SupplierOrderItem
from playitloud.models.supplier_order import RestockStatus
from playitloud.repositories.album_repository import AlbumRepository
from playitloud.repositories.supplier_offer_repository import SupplierOfferRepository
from playitloud.repositories.supplier_order_repository import SupplierOrderRepository
from playitloud.repositories.supplier_repository import SupplierRepository
from playitloud.schemas.supplier_order import (
    RestockStatusUpdate,
    SupplierOrderCreate,
    SupplierOrderRead,
)


class SupplierOrderService:
    def __init__(
        self,
        session: Session,
        supplier_order_repository: SupplierOrderRepository,
        supplier_repository: SupplierRepository,
        album_repository: AlbumRepository,
        supplier_offer_repository: SupplierOfferRepository,
    ) -> None:
        self.session = session
        self.supplier_order_repository = supplier_order_repository
        self.supplier_repository = supplier_repository
        self.album_repository = album_repository
        self.supplier_offer_repository = supplier_offer_repository

    def create_supplier_order(
        self, supplier_id: int, supplier_order_create: SupplierOrderCreate
    ) -> SupplierOrderRead:
        if not self.supplier_repository.get_by_id(supplier_id):
            raise ValueError(f"Supplier with id {supplier_id} not found.")

        album_ids = [item.album_id for item in supplier_order_create.items]

        if len(album_ids) != len(set(album_ids)):
            raise ValueError("Duplicate album in supplier order items.")

        supplier_order_items: list[SupplierOrderItem] = []
        total_price = 0

        for item in supplier_order_create.items:
            offer = self.supplier_offer_repository.get_by_supplier_and_album(
                supplier_id, item.album_id
            )

            if not offer:
                raise ValueError(f"Supplier offer for album {item.album_id} not found.")

            total_price += item.quantity * offer.unit_price

            supplier_order_items.append(
                SupplierOrderItem(
                    album_id=item.album_id,
                    quantity=item.quantity,
                    unit_price=offer.unit_price,
                )
            )

        supplier_order = SupplierOrder(
            supplier_id=supplier_id,
            status=RestockStatus.PENDING,
            total_price=total_price,
        )
        supplier_order.supplier_order_items = supplier_order_items

        self.supplier_order_repository.add(supplier_order)
        self.session.commit()

        return self.get_supplier_order(supplier_id, supplier_order.id)

    def get_supplier_order(self, supplier_id: int, supplier_order_id: int) -> SupplierOrderRead:
        supplier_order = self.supplier_order_repository.get_by_id_and_supplier_id(
            supplier_order_id, supplier_id
        )

        if not supplier_order:
            raise ValueError("Supplier order not found.")

        return SupplierOrderRead.model_validate(supplier_order)

    def get_supplier_orders(self, supplier_id: int) -> list[SupplierOrderRead]:
        if not self.supplier_repository.get_by_id(supplier_id):
            raise ValueError(f"Supplier with id {supplier_id} not found.")

        supplier_orders = self.supplier_order_repository.get_all_by_supplier_id(supplier_id)

        return [SupplierOrderRead.model_validate(o) for o in supplier_orders]

    def update_supplier_order_status(
        self, supplier_id: int, supplier_order_id: int, restock_status_update: RestockStatusUpdate
    ) -> SupplierOrderRead:
        supplier_order = self.supplier_order_repository.get_by_id_and_supplier_id(
            supplier_order_id, supplier_id
        )

        if not supplier_order:
            raise ValueError("Supplier order not found.")

        if (
            restock_status_update.status == RestockStatus.RECEIVED
            and supplier_order.status != RestockStatus.RECEIVED
        ):
            for item in supplier_order.supplier_order_items:
                album = self.album_repository.get_by_id(item.album_id)

                if not album:
                    raise ValueError(f"Album with id {item.album_id} not found.")

                album.stock += item.quantity

        supplier_order.status = restock_status_update.status

        self.session.commit()

        return self.get_supplier_order(supplier_id, supplier_order_id)

    def delete_supplier_order(self, supplier_id: int, supplier_order_id: int) -> None:
        supplier_order = self.supplier_order_repository.get_by_id_and_supplier_id(
            supplier_order_id, supplier_id
        )

        if not supplier_order:
            raise ValueError("Supplier order not found.")

        self.supplier_order_repository.delete(supplier_order)
        self.session.commit()
