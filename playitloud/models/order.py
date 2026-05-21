from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Enum as SQLEnum, ForeignKeyConstraint, Numeric, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from playitloud.models import Base

if TYPE_CHECKING:
    from playitloud.models import User, Address, OrderItem, Invoice

class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order(Base):
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    
    address_id: Mapped[int] = mapped_column(nullable=False)
    
    status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus, name="order_status", native_enum=True),
        nullable=False,
        default=OrderStatus.PENDING.value,
    )
    
    total_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    
    user: Mapped["User"] = relationship(back_populates="orders")
    
    address: Mapped["Address"] = relationship(back_populates="orders")
    
    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )
    
    invoice: Mapped["Invoice | None"] = relationship(
        back_populates="order",
        uselist=False,
    )
    
    __table_args__ = (
        CheckConstraint("total_price > 0", name="chk_orders_total_price_positive"),
        ForeignKeyConstraint(
            ["address_id", "user_id"],
            ["addresses.id", "addresses.user_id"],
            name="fk_orders_address_owner",
        ),
    )
    