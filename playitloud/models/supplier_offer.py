from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from playitloud.models.base import Base

if TYPE_CHECKING:
    from playitloud.models.album import Album
    from playitloud.models.supplier import Supplier

class SupplierOffer(Base):
    __tablename__ = "supplier_offers"
    
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id"),
        primary_key=True,
    )
    
    album_id: Mapped[int] = mapped_column(
        ForeignKey("albums.id"),
        primary_key=True,
    )
    
    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    
    supplier: Mapped["Supplier"] = relationship(back_populates="supplier_offers")
    
    album: Mapped["Album"] = relationship(back_populates="supplier_offers")
    
    __table_args__ = (
        CheckConstraint("unit_price > 0", name="chk_supplier_offers_unit_price_positive"),
    )