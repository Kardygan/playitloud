from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from playitloud.core.constants import MAX_EMAIL_LENGTH, MAX_SUPPLIER_NAME_LENGTH
from playitloud.models import Base

if TYPE_CHECKING:
    from playitloud.models import SupplierOffer, SupplierOrder

class Supplier(Base):
    __tablename__ = "suppliers"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str] = mapped_column(
        String(MAX_SUPPLIER_NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    contact_email: Mapped[str | None] = mapped_column(
        String(MAX_EMAIL_LENGTH),
        nullable=True,
        unique=True,
    )
    
    supplier_offers: Mapped[list["SupplierOffer"]] = relationship(back_populates="supplier")
    
    supplier_orders: Mapped[list["SupplierOrder"]] = relationship(back_populates="supplier")