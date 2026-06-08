from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing	 import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Numeric, CheckConstraint, Enum as SQLEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from playitloud.models import Base

if TYPE_CHECKING:
    from playitloud.models import Supplier, SupplierOrderItem

class RestockStatus(str, Enum):
    PENDING = "pending"
    ORDERED = "ordered"
    RECEIVED = "received"
    CANCELLED = "cancelled"

class SupplierOrder(Base):
    __tablename__ = "supplier_orders"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id"),
        nullable=False,
    )
    
    status: Mapped[RestockStatus] = mapped_column(
        SQLEnum(RestockStatus, name="restock_status", native_enum=True),
        nullable=False,
        default=RestockStatus.PENDING,
    )
    
    total_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    
    supplier: Mapped["Supplier"] = relationship(back_populates="supplier_orders")
    
    supplier_order_items: Mapped[list["SupplierOrderItem"]] = relationship(back_populates="supplier_order")
    
    __table_args__ = (
        CheckConstraint("total_price > 0", name="chk_supplier_orders_total_price_positive"),
    )