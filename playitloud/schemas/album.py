from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from playitloud.core.constants import MAX_ALBUM_NAME_LENGTH
from playitloud.models.album import MediaType
from playitloud.schemas.artist import ArtistRead


class AlbumCreate(BaseModel):
    name: str = Field(max_length=MAX_ALBUM_NAME_LENGTH)
    description: str | None = None
    cover_url: str | None = None
    media_type: MediaType
    price: Decimal = Field(gt=0)
    stock: int = Field(ge=0, default=0)
    artist_ids: list[int] = []


class AlbumRead(BaseModel):
    id: int
    name: str
    description: str | None
    cover_url: str | None
    media_type: MediaType
    price: Decimal
    stock: int
    created_at: datetime
    updated_at: datetime
    artists: list[ArtistRead]

    model_config = ConfigDict(from_attributes=True)


class AlbumUpdate(BaseModel):
    name: str = Field(max_length=MAX_ALBUM_NAME_LENGTH)
    description: str | None = None
    cover_url: str | None = None
    price: Decimal = Field(gt=0)
    stock: int = Field(ge=0, default=0)
    artist_ids: list[int] = []
