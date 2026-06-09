from pydantic import BaseModel, ConfigDict, Field, field_validator

from playitloud.core.constants import DEFAULT_IMAGE_URL, MAX_ARTIST_NAME_LENGTH
from playitloud.schemas.types import NonBlankStr


class ArtistCreate(BaseModel):
    name: NonBlankStr = Field(max_length=MAX_ARTIST_NAME_LENGTH)
    picture_url: str | None = None
    description: str | None = None


class ArtistRead(BaseModel):
    id: int
    name: str
    picture_url: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("picture_url", mode="before")
    @classmethod
    def _default_picture_url(cls, value: str | None) -> str:
        return value or DEFAULT_IMAGE_URL


class ArtistUpdate(BaseModel):
    name: NonBlankStr = Field(max_length=MAX_ARTIST_NAME_LENGTH)
    picture_url: str | None = None
    description: str | None = None
