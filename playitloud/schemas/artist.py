from pydantic import BaseModel, ConfigDict, Field

from playitloud.core.constants import MAX_ARTIST_NAME_LENGTH


class ArtistCreate(BaseModel):
    name: str = Field(max_length=MAX_ARTIST_NAME_LENGTH)
    picture_url: str | None = None
    description: str | None = None


class ArtistRead(BaseModel):
    id: int
    name: str
    picture_url: str | None
    description: str | None

    model_config = ConfigDict(from_attributes=True)


class ArtistUpdate(BaseModel):
    name: str = Field(max_length=MAX_ARTIST_NAME_LENGTH)
    picture_url: str | None = None
    description: str | None = None
