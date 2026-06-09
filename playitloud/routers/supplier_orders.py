from fastapi import APIRouter, Depends, Response, status

from playitloud.deps import get_supplier_order_service
from playitloud.schemas.supplier_order import (
    RestockStatusUpdate,
    SupplierOrderCreate,
    SupplierOrderRead,
)
from playitloud.services.supplier_order_service import SupplierOrderService

router = APIRouter(prefix="/suppliers/{supplier_id}/orders", tags=["supplier-orders"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=SupplierOrderRead)
def create_supplier_order(
    supplier_id: int,
    supplier_order_create: SupplierOrderCreate,
    response: Response,
    service: SupplierOrderService = Depends(get_supplier_order_service),
):
    supplier_order = service.create_supplier_order(supplier_id, supplier_order_create)
    response.headers["Location"] = f"/suppliers/{supplier_id}/orders/{supplier_order.id}"

    return supplier_order


@router.get("", response_model=list[SupplierOrderRead])
def list_supplier_orders(
    supplier_id: int,
    service: SupplierOrderService = Depends(get_supplier_order_service),
):
    return service.get_supplier_orders(supplier_id)


@router.get("/{supplier_order_id}", response_model=SupplierOrderRead)
def get_supplier_order(
    supplier_id: int,
    supplier_order_id: int,
    service: SupplierOrderService = Depends(get_supplier_order_service),
):
    return service.get_supplier_order(supplier_id, supplier_order_id)


@router.patch("/{supplier_order_id}", response_model=SupplierOrderRead)
def update_supplier_order_status(
    supplier_id: int,
    supplier_order_id: int,
    restock_status_update: RestockStatusUpdate,
    service: SupplierOrderService = Depends(get_supplier_order_service),
):
    return service.update_supplier_order_status(
        supplier_id, supplier_order_id, restock_status_update
    )


@router.delete(
    "/{supplier_order_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
def delete_supplier_order(
    supplier_id: int,
    supplier_order_id: int,
    service: SupplierOrderService = Depends(get_supplier_order_service),
):
    service.delete_supplier_order(supplier_id, supplier_order_id)
