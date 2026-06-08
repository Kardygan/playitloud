from sqlalchemy.orm import Session

from playitloud.models import Order, OrderItem
from playitloud.models.order import OrderStatus
from playitloud.repositories.album_repository import AlbumRepository
from playitloud.repositories.address_repository import AddressRepository
from playitloud.repositories.order_repository import OrderRepository
from playitloud.repositories.user_repository import UserRepository
from playitloud.schemas.order import OrderCreate, OrderRead, OrderStatusUpdate


class OrderService:
    def __init__(
        self,
        session: Session,
        order_repository: OrderRepository,
        user_repository: UserRepository,
        address_repository: AddressRepository,
        album_repository: AlbumRepository,
    ) -> None:
        self.session = session
        self.order_repository = order_repository
        self.user_repository = user_repository
        self.address_repository = address_repository
        self.album_repository = album_repository

    def create_order(self, user_id: int, order_create: OrderCreate) -> OrderRead:
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise ValueError("User not found.")

        address = self.address_repository.get_by_id_and_user_id(order_create.address_id, user_id)

        if not address:
            raise ValueError("Address not found.")

        album_ids = [item.album_id for item in order_create.items]

        if len(album_ids) != len(set(album_ids)):
            raise ValueError("Duplicate album in order items.")

        order_items: list[OrderItem] = []
        total_price = 0

        for item in order_create.items:
            album = self.album_repository.get_by_id(item.album_id)

            if not album:
                raise ValueError(f"Album with id {item.album_id} not found.")

            if album.stock < item.quantity:
                raise ValueError(f"Insufficient stock for album {item.album_id}.")

            album.stock -= item.quantity
            total_price += item.quantity * album.price

            order_items.append(
                OrderItem(
                    album_id=album.id,
                    quantity=item.quantity,
                    unit_price=album.price,
                )
            )

        order = Order(
            user_id=user_id,
            address_id=address.id,
            status=OrderStatus.PENDING,
            total_price=total_price,
        )
        order.order_items = order_items

        self.order_repository.add(order)
        self.session.commit()

        return self.get_order(user_id, order.id)

    def get_order(self, user_id: int, order_id: int) -> OrderRead:
        order = self.order_repository.get_by_id_and_user_id(order_id, user_id)

        if not order:
            raise ValueError("Order not found.")

        return OrderRead.model_validate(order)

    def get_user_orders(self, user_id: int) -> list[OrderRead]:
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise ValueError("User not found.")

        orders = self.order_repository.get_all_by_user_id(user_id)

        return [OrderRead.model_validate(o) for o in orders]

    def update_order_status(
        self, user_id: int, order_id: int, order_status_update: OrderStatusUpdate
    ) -> OrderRead:
        order = self.order_repository.get_by_id_and_user_id(order_id, user_id)

        if not order:
            raise ValueError("Order not found.")

        order.status = order_status_update.status

        self.session.commit()

        return self.get_order(user_id, order_id)

    def delete_order(self, user_id: int, order_id: int) -> None:
        order = self.order_repository.get_by_id_and_user_id(order_id, user_id)

        if not order:
            raise ValueError("Order not found.")

        self.order_repository.delete(order)
        self.session.commit()
