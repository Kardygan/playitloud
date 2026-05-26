from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from playitloud.core.constants import MAX_ARTIST_NAME_LENGTH
from playitloud.models import Base

if TYPE_CHECKING:
    from playitloud.models import Album

class Artist(Base):
    __tablename__ = "artists"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str] = mapped_column(
        String(MAX_ARTIST_NAME_LENGTH),
        nullable=False,
    )

    picture_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    
    albums: Mapped[list["Album"]] = relationship(
        "Album",
        secondary="album_artists",
        back_populates="artists",
    )