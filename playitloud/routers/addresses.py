from fastapi import APIRouter, Depends, Response, status

from playitloud.deps import get_address_service
from playitloud.schemas.address import AddressCreate, AddressRead, AddressUpdate
from playitloud.services.address_service import AddressService

router = APIRouter(prefix="/users/{user_id}/addresses", tags=["addresses"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=AddressRead)
def create_address(
    user_id: int,
    address_create: AddressCreate,
    response: Response,
    service: AddressService = Depends(get_address_service),
):
    address = service.create_address(user_id, address_create)
    response.headers["Location"] = f"/users/{user_id}/addresses/{address.id}"
    return address


@router.get("", response_model=list[AddressRead])
def list_addresses(
    user_id: int,
    service: AddressService = Depends(get_address_service),
):
    return service.get_user_addresses(user_id)


@router.get("/{address_id}", response_model=AddressRead)
def get_address(
    user_id: int,
    address_id: int,
    service: AddressService = Depends(get_address_service),
):
    return service.get_address(user_id, address_id)


@router.put("/{address_id}", response_model=AddressRead)
def update_address(
    user_id: int,
    address_id: int,
    address_update: AddressUpdate,
    service: AddressService = Depends(get_address_service),
):
    return service.update_address(user_id, address_id, address_update)


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_address(
    user_id: int,
    address_id: int,
    service: AddressService = Depends(get_address_service),
):
    service.delete_address(user_id, address_id)
