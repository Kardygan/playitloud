from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String, Text, Enum as SQLEnum, Numeric, DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from playitloud.core.constants import MAX_ALBUM_NAME_LENGTH
from playitloud.models import Base

if TYPE_CHECKING:
    from playitloud.models import Artist, OrderItem, SupplierOffer, SupplierOrderItem

class MediaType(str, Enum):
    CD = "cd"
    VINYL = "vinyl"

class Album(Base):
    __tablename__ = "albums"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str] = mapped_column(
        String(MAX_ALBUM_NAME_LENGTH),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    cover_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    
    media_type: Mapped[MediaType] = mapped_column(
        SQLEnum(MediaType, name="media_type", native_enum=True), 
        nullable=False,
    )
    
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    
    stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False, 
        server_default="0",
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
    
    artists: Mapped[list["Artist"]] = relationship(
        "Artist",
        secondary="album_artists",
        back_populates="albums",
    )
    
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="album")
    
    supplier_offers: Mapped[list["SupplierOffer"]] = relationship(back_populates="album")
    
    supplier_order_items: Mapped[list["SupplierOrderItem"]] = relationship(back_populates="album")
    
    __table_args__ = (
        CheckConstraint("price > 0", name="chk_albums_price_positive"),
        CheckConstraint("stock >= 0", name="chk_albums_stock_positive"),
    )