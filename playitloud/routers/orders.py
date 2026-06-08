from fastapi import APIRouter, Depends, Response, status

from playitloud.deps import get_order_service
from playitloud.schemas.order import OrderCreate, OrderRead, OrderStatusUpdate
from playitloud.services.order_service import OrderService

router = APIRouter(prefix="/users/{user_id}/orders", tags=["orders"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=OrderRead)
def create_order(
    user_id: int,
    order_create: OrderCreate,
    response: Response,
    service: OrderService = Depends(get_order_service),
):
    order = service.create_order(user_id, order_create)
    response.headers["Location"] = f"/users/{user_id}/orders/{order.id}"
    return order


@router.get("", response_model=list[OrderRead])
def list_orders(
    user_id: int,
    service: OrderService = Depends(get_order_service),
):
    return service.get_user_orders(user_id)


@router.get("/{order_id}", response_model=OrderRead)
def get_order(
    user_id: int,
    order_id: int,
    service: OrderService = Depends(get_order_service),
):
    return service.get_order(user_id, order_id)


@router.patch("/{order_id}", response_model=OrderRead)
def update_order_status(
    user_id: int,
    order_id: int,
    order_status_update: OrderStatusUpdate,
    service: OrderService = Depends(get_order_service),
):
    return service.update_order_status(user_id, order_id, order_status_update)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_order(
    user_id: int,
    order_id: int,
    service: OrderService = Depends(get_order_service),
):
    service.delete_order(user_id, order_id)
