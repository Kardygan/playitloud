from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from playitloud.models import Order


class OrderRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, order: Order) -> None:
        self.session.add(order)

    def get_by_id_and_user_id(self, order_id: int, user_id: int) -> Order | None:
        statement = (
            select(Order)
            .where(
                Order.id == order_id,
                Order.user_id == user_id,
            )
            .options(selectinload(Order.order_items))
        )

        return self.session.scalar(statement)

    def get_all_by_user_id(self, user_id: int) -> list[Order]:
        statement = (
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.order_items))
        )

        return list(self.session.scalars(statement).all())

    def delete(self, order: Order) -> None:
        self.session.delete(order)
