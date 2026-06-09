from sqlalchemy import select
from sqlalchemy.orm import Session

from playitloud.models import SupplierOffer


class SupplierOfferRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, supplier_offer: SupplierOffer) -> None:
        self.session.add(supplier_offer)

    def get_by_supplier_and_album(
        self, supplier_id: int, album_id: int
    ) -> SupplierOffer | None:
        statement = select(SupplierOffer).where(
            SupplierOffer.supplier_id == supplier_id,
            SupplierOffer.album_id == album_id,
        )

        return self.session.scalar(statement)

    def get_all_by_supplier_id(self, supplier_id: int) -> list[SupplierOffer]:
        statement = select(SupplierOffer).where(SupplierOffer.supplier_id == supplier_id)

        return list(self.session.scalars(statement).all())

    def delete(self, supplier_offer: SupplierOffer) -> None:
        self.session.delete(supplier_offer)
