from sqlalchemy.orm import Session

from playitloud.models import Album, Artist
from playitloud.repositories.album_repository import AlbumRepository
from playitloud.repositories.artist_repository import ArtistRepository
from playitloud.schemas.album import AlbumCreate, AlbumRead, AlbumUpdate


class AlbumService:
    def __init__(
        self,
        session: Session,
        album_repository: AlbumRepository,
        artist_repository: ArtistRepository,
    ) -> None:
        self.session = session
        self.album_repository = album_repository
        self.artist_repository = artist_repository

    def _resolve_artists(self, artist_ids: list[int]) -> list[Artist]:
        if not artist_ids:
            return []
        
        artists = self.artist_repository.get_all_by_ids(artist_ids)
        
        if len(artists) != len(artist_ids):
            found_ids = {a.id for a in artists}
            missing_id = next(i for i in artist_ids if i not in found_ids)
            
            raise ValueError(f"Artist with id {missing_id} not found.")
        
        return artists

    def create_album(self, album_create: AlbumCreate) -> AlbumRead:
        artists = self._resolve_artists(album_create.artist_ids)
        
        album = Album(
            name=album_create.name,
            description=album_create.description,
            cover_url=album_create.cover_url,
            media_type=album_create.media_type,
            price=album_create.price,
            stock=album_create.stock,
        )
        
        album.artists = artists
        self.album_repository.add(album)
        self.session.commit()
        
        return self.get_album_by_id(album.id)

    def get_album_by_id(self, album_id: int) -> AlbumRead:
        album = self.album_repository.get_by_id(album_id)
        
        if not album:
            raise ValueError(f"Album with id {album_id} not found.")
        
        return AlbumRead.model_validate(album)
    
    def get_albums_by_artist(self, artist_id: int) -> list[AlbumRead]:
        artist = self.artist_repository.get_by_id(artist_id)
        
        if not artist:
            raise ValueError(f"Artist with id {artist_id} not found.")
        
        albums = self.album_repository.get_all_by_artist_id(artist_id)
        
        return [AlbumRead.model_validate(a) for a in albums]

    def get_all_albums(self) -> list[AlbumRead]:
        return [AlbumRead.model_validate(a) for a in self.album_repository.get_all()]

    def update_album(self, album_id: int, album_update: AlbumUpdate) -> AlbumRead:
        album = self.album_repository.get_by_id(album_id)
        
        if not album:
            raise ValueError(f"Album with id {album_id} not found.")
        
        artists = self._resolve_artists(album_update.artist_ids)
        
        album.name = album_update.name
        album.description = album_update.description
        album.cover_url = album_update.cover_url
        album.price = album_update.price
        album.stock = album_update.stock
        album.artists = artists
        
        self.session.commit()
        
        return self.get_album_by_id(album_id)

    def delete_album(self, album_id: int) -> None:
        album = self.album_repository.get_by_id(album_id)
        
        if not album:
            raise ValueError(f"Album with id {album_id} not found.")
        
        self.album_repository.delete(album)
        self.session.commit()
