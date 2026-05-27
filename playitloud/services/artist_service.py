from sqlalchemy.orm import Session

from playitloud.models import Artist
from playitloud.repositories.artist_repository import ArtistRepository
from playitloud.schemas.artist import ArtistCreate, ArtistRead, ArtistUpdate


class ArtistService:
    def __init__(self, session: Session, artist_repository: ArtistRepository) -> None:
        self.session = session
        self.artist_repository = artist_repository

    def create_artist(self, artist_create: ArtistCreate) -> ArtistRead:
        artist = Artist(
            name=artist_create.name,
            picture_url=artist_create.picture_url,
            description=artist_create.description,
        )
        
        self.artist_repository.add(artist)
        self.session.commit()
        self.session.refresh(artist)
        
        return ArtistRead.model_validate(artist)

    def get_artist_by_id(self, artist_id: int) -> ArtistRead:
        artist = self.artist_repository.get_by_id(artist_id)
        
        if not artist:
            raise ValueError(f"Artist with id {artist_id} not found.")
        
        return ArtistRead.model_validate(artist)

    def get_all_artists(self) -> list[ArtistRead]:
        return [ArtistRead.model_validate(a) for a in self.artist_repository.get_all()]

    def update_artist(self, artist_id: int, artist_update: ArtistUpdate) -> ArtistRead:
        artist = self.artist_repository.get_by_id(artist_id)
        
        if not artist:
            raise ValueError(f"Artist with id {artist_id} not found.")
        
        artist.name = artist_update.name
        artist.picture_url = artist_update.picture_url
        artist.description = artist_update.description
        
        self.session.commit()
        self.session.refresh(artist)
        
        return ArtistRead.model_validate(artist)

    def delete_artist(self, artist_id: int) -> None:
        artist = self.artist_repository.get_by_id(artist_id)
        
        if not artist:
            raise ValueError(f"Artist with id {artist_id} not found.")
        
        self.artist_repository.delete(artist)
        self.session.commit()
