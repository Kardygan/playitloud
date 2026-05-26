from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from playitloud.core.constants import (
    MAX_CITY_LENGTH,
    MAX_COUNTRY_CODE_LENGTH,
    MAX_POSTAL_CODE_LENGTH,
    MAX_STREET_LENGTH,
)
from playitloud.models import Base

if TYPE_CHECKING:
    from playitloud.models import User, Order

class Address(Base):
    __tablename__ = "addresses"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    
    street: Mapped[str] = mapped_column(
        String(MAX_STREET_LENGTH),
        nullable=False,
    )

    city: Mapped[str] = mapped_column(
        String(MAX_CITY_LENGTH),
        nullable=False,
    )

    postal_code: Mapped[str] = mapped_column(
        String(MAX_POSTAL_CODE_LENGTH),
        nullable=False,
    )

    country_code: Mapped[str] = mapped_column(
        String(MAX_COUNTRY_CODE_LENGTH),
        nullable=False,
    )
    
    user: Mapped["User"] = relationship(back_populates="addresses")
    
    orders: Mapped[list["Order"]] = relationship(
        back_populates="address",
        primaryjoin="Order.address_id == Address.id",
        foreign_keys="[Order.address_id]",
        overlaps="user,orders",
    )
    
    __table_args__ = (
        UniqueConstraint(
            "id",
            "user_id",
            name="uq_addresses_id_user",
        ),
    )