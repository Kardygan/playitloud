from fastapi import APIRouter, Depends, Response, status

from playitloud.deps import get_supplier_offer_service
from playitloud.schemas.supplier_offer import (
    SupplierOfferCreate,
    SupplierOfferRead,
    SupplierOfferUpdate,
)
from playitloud.services.supplier_offer_service import SupplierOfferService

router = APIRouter(prefix="/suppliers/{supplier_id}/offers", tags=["supplier-offers"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=SupplierOfferRead)
def create_offer(
    supplier_id: int,
    supplier_offer_create: SupplierOfferCreate,
    response: Response,
    service: SupplierOfferService = Depends(get_supplier_offer_service),
):
    offer = service.create_offer(supplier_id, supplier_offer_create)
    response.headers["Location"] = f"/suppliers/{supplier_id}/offers/{offer.album_id}"

    return offer


@router.get("", response_model=list[SupplierOfferRead])
def list_offers(
    supplier_id: int,
    service: SupplierOfferService = Depends(get_supplier_offer_service),
):
    return service.get_supplier_offers(supplier_id)


@router.get("/{album_id}", response_model=SupplierOfferRead)
def get_offer(
    supplier_id: int,
    album_id: int,
    service: SupplierOfferService = Depends(get_supplier_offer_service),
):
    return service.get_offer(supplier_id, album_id)


@router.put("/{album_id}", response_model=SupplierOfferRead)
def update_offer(
    supplier_id: int,
    album_id: int,
    supplier_offer_update: SupplierOfferUpdate,
    service: SupplierOfferService = Depends(get_supplier_offer_service),
):
    return service.update_offer(supplier_id, album_id, supplier_offer_update)


@router.delete("/{album_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_offer(
    supplier_id: int,
    album_id: int,
    service: SupplierOfferService = Depends(get_supplier_offer_service),
):
    service.delete_offer(supplier_id, album_id)
