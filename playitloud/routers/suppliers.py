from fastapi import APIRouter, Depends, Response, status

from playitloud.deps import get_supplier_service
from playitloud.schemas.supplier import SupplierCreate, SupplierRead, SupplierUpdate
from playitloud.services.supplier_service import SupplierService

router = APIRouter(prefix="/suppliers", tags=["suppliers"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=SupplierRead)
def create_supplier(
    supplier_create: SupplierCreate,
    response: Response,
    service: SupplierService = Depends(get_supplier_service),
):
    supplier = service.create_supplier(supplier_create)
    response.headers["Location"] = f"/suppliers/{supplier.id}"

    return supplier


@router.get("", response_model=list[SupplierRead])
def list_suppliers(service: SupplierService = Depends(get_supplier_service)):
    return service.get_all_suppliers()


@router.get("/{supplier_id}", response_model=SupplierRead)
def get_supplier(supplier_id: int, service: SupplierService = Depends(get_supplier_service)):
    return service.get_supplier_by_id(supplier_id)


@router.patch("/{supplier_id}", response_model=SupplierRead)
def update_supplier(
    supplier_id: int,
    supplier_update: SupplierUpdate,
    service: SupplierService = Depends(get_supplier_service),
):
    return service.update_supplier(supplier_id, supplier_update)


@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_supplier(supplier_id: int, service: SupplierService = Depends(get_supplier_service)):
    service.delete_supplier(supplier_id)
