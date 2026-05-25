from sqlalchemy import select
from sqlalchemy.orm import Session

from playitloud.models import Address


class AddressRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, address: Address) -> None:
        self.session.add(address)

    def get_by_id_and_user_id(self, address_id: int, user_id: int) -> Address | None:
        statement = select(Address).where(
            Address.id == address_id,
            Address.user_id == user_id,
        )

        return self.session.scalar(statement)

    def get_all_by_user_id(self, user_id: int) -> list[Address]:
        statement = select(Address).where(Address.user_id == user_id)

        return list(self.session.scalars(statement).all())

    def delete(self, address: Address) -> None:
        self.session.delete(address)
