from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import CheckConstraint, String, Text, Enum as SQLEnum, Numeric, DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING
from playitloud.models.base import Base

if TYPE_CHECKING:
    from playitloud.models.artist import Artist

class MediaType(str, Enum):
    CD = "cd"
    VINYL = "vinyl"

class Album(Base):
    __tablename__ = "albums"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    
    cover_url: Mapped[str | None] = mapped_column(
        String(255),
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
        server_default=0,
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
    
    artists: Mapped[list["Artist"]] = relationship(
        "Artist",
        secondary="album_artists",
        back_populates="albums",
    )
    
    __table_args__ = (
        CheckConstraint("price > 0", name="chk_albums_price_positive"),
        CheckConstraint("stock >= 0", name="chk_albums_stock_positive"),
    )