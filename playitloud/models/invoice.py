from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from playitloud.models import Base

if TYPE_CHECKING:
    from playitloud.models import Order

class Invoice(Base):
    __tablename__ = "invoices"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
        unique=True,
    )
    
    invoice_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )
    
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    
    issued_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    
    order: Mapped["Order"] = relationship(back_populates="invoice")
    
    __table_args__ = (
        CheckConstraint("total_amount > 0", name="chk_invoices_total_amount_positive"),
    )