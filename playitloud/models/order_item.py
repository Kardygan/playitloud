from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from playitloud.models import Base

if TYPE_CHECKING:
    from playitloud.models import Order, Album

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
    )
    
    album_id: Mapped[int] = mapped_column(
        ForeignKey("albums.id"),
        nullable=False,
    )
    
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    
    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    
    order: Mapped["Order"] = relationship(
        back_populates="order_items",
    )
    
    album: Mapped["Album"] = relationship(
        back_populates="order_items",
    )
    
    __table_args__ = (
        CheckConstraint("quantity > 0", name="chk_order_items_quantity_positive"),
        CheckConstraint("unit_price > 0", name="chk_order_items_unit_price_positive"),
    )