from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from playitloud.core.constants import DEFAULT_IMAGE_URL, MAX_ALBUM_NAME_LENGTH, MAX_PRICE
from playitloud.models.album import MediaType
from playitloud.schemas.artist import ArtistRead
from playitloud.schemas.types import NonBlankStr


class AlbumCreate(BaseModel):
    name: NonBlankStr = Field(max_length=MAX_ALBUM_NAME_LENGTH)
    description: str | None = None
    cover_url: str | None = None
    media_type: MediaType
    price: Decimal = Field(gt=0, le=MAX_PRICE, max_digits=10, decimal_places=2)
    stock: int = Field(ge=0, default=0)
    artist_ids: list[int] = []


class AlbumRead(BaseModel):
    id: int
    name: str
    description: str | None
    cover_url: str
    media_type: MediaType
    price: Decimal
    stock: int
    created_at: datetime
    updated_at: datetime
    artists: list[ArtistRead]

    model_config = ConfigDict(from_attributes=True)

    @field_validator("cover_url", mode="before")
    @classmethod
    def _default_cover_url(cls, value: str | None) -> str:
        return value or DEFAULT_IMAGE_URL


class AlbumUpdate(BaseModel):
    name: NonBlankStr = Field(max_length=MAX_ALBUM_NAME_LENGTH)
    description: str | None = None
    cover_url: str | None = None
    price: Decimal = Field(gt=0, le=MAX_PRICE, max_digits=10, decimal_places=2)
    stock: int = Field(ge=0, default=0)
    artist_ids: list[int] = []
