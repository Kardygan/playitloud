from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from playitloud.models import Base

if TYPE_CHECKING:
    from playitloud.models import SupplierOrder, Album

class SupplierOrderItem(Base):
    __tablename__ = "supplier_order_items"
    
    supplier_order_id: Mapped[int] = mapped_column(
        ForeignKey("supplier_orders.id"),
        primary_key=True,
    )
    
    album_id: Mapped[int] = mapped_column(
        ForeignKey("albums.id"),
        primary_key=True,
    )
    
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    
    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    
    supplier_order: Mapped["SupplierOrder"] = relationship(back_populates="supplier_order_items")
    
    album: Mapped["Album"] = relationship(back_populates="supplier_order_items")
    
    __table_args__ = (
        CheckConstraint("quantity > 0", name="chk_supplier_order_items_quantity_positive"),
        CheckConstraint("unit_price > 0", name="chk_supplier_order_items_unit_price_positive"),
    )