from sqlalchemy.orm import Session

from playitloud.models import SupplierOffer
from playitloud.repositories.album_repository import AlbumRepository
from playitloud.repositories.supplier_offer_repository import SupplierOfferRepository
from playitloud.repositories.supplier_repository import SupplierRepository
from playitloud.schemas.supplier_offer import (
    SupplierOfferCreate,
    SupplierOfferRead,
    SupplierOfferUpdate,
)


class SupplierOfferService:
    def __init__(
        self,
        session: Session,
        supplier_offer_repository: SupplierOfferRepository,
        supplier_repository: SupplierRepository,
        album_repository: AlbumRepository,
    ) -> None:
        self.session = session
        self.supplier_offer_repository = supplier_offer_repository
        self.supplier_repository = supplier_repository
        self.album_repository = album_repository

    def create_offer(
        self, supplier_id: int, supplier_offer_create: SupplierOfferCreate
    ) -> SupplierOfferRead:
        if not self.supplier_repository.get_by_id(supplier_id):
            raise ValueError(f"Supplier with id {supplier_id} not found.")

        if not self.album_repository.get_by_id(supplier_offer_create.album_id):
            raise ValueError(f"Album with id {supplier_offer_create.album_id} not found.")

        if self.supplier_offer_repository.get_by_supplier_and_album(
            supplier_id, supplier_offer_create.album_id
        ):
            raise ValueError(
                f"Offer for album {supplier_offer_create.album_id} already exists."
            )

        supplier_offer = SupplierOffer(
            supplier_id=supplier_id,
            album_id=supplier_offer_create.album_id,
            unit_price=supplier_offer_create.unit_price,
        )

        self.supplier_offer_repository.add(supplier_offer)
        self.session.commit()
        self.session.refresh(supplier_offer)

        return SupplierOfferRead.model_validate(supplier_offer)

    def get_offer(self, supplier_id: int, album_id: int) -> SupplierOfferRead:
        supplier_offer = self.supplier_offer_repository.get_by_supplier_and_album(
            supplier_id, album_id
        )

        if not supplier_offer:
            raise ValueError(f"Offer for album {album_id} not found.")

        return SupplierOfferRead.model_validate(supplier_offer)

    def get_supplier_offers(self, supplier_id: int) -> list[SupplierOfferRead]:
        if not self.supplier_repository.get_by_id(supplier_id):
            raise ValueError(f"Supplier with id {supplier_id} not found.")

        offers = self.supplier_offer_repository.get_all_by_supplier_id(supplier_id)

        return [SupplierOfferRead.model_validate(o) for o in offers]

    def update_offer(
        self, supplier_id: int, album_id: int, supplier_offer_update: SupplierOfferUpdate
    ) -> SupplierOfferRead:
        supplier_offer = self.supplier_offer_repository.get_by_supplier_and_album(
            supplier_id, album_id
        )

        if not supplier_offer:
            raise ValueError(f"Offer for album {album_id} not found.")

        supplier_offer.unit_price = supplier_offer_update.unit_price

        self.session.commit()
        self.session.refresh(supplier_offer)

        return SupplierOfferRead.model_validate(supplier_offer)

    def delete_offer(self, supplier_id: int, album_id: int) -> None:
        supplier_offer = self.supplier_offer_repository.get_by_supplier_and_album(
            supplier_id, album_id
        )

        if not supplier_offer:
            raise ValueError(f"Offer for album {album_id} not found.")

        self.supplier_offer_repository.delete(supplier_offer)
        self.session.commit()
