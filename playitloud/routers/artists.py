from fastapi import APIRouter, Depends, Response, status

from playitloud.deps import get_album_service, get_artist_service
from playitloud.schemas.album import AlbumRead
from playitloud.schemas.artist import ArtistCreate, ArtistRead, ArtistUpdate
from playitloud.services.album_service import AlbumService
from playitloud.services.artist_service import ArtistService

router = APIRouter(prefix="/artists", tags=["artists"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ArtistRead)
def create_artist(
    payload: ArtistCreate,
    response: Response,
    service: ArtistService = Depends(get_artist_service),
):
    artist = service.create_artist(payload)
    response.headers["Location"] = f"/artists/{artist.id}"
    
    return artist


@router.get("", response_model=list[ArtistRead])
def list_artists(service: ArtistService = Depends(get_artist_service)):
    return service.get_all_artists()


@router.get("/{artist_id}", response_model=ArtistRead)
def get_artist(artist_id: int, service: ArtistService = Depends(get_artist_service)):
    return service.get_artist_by_id(artist_id)


@router.patch("/{artist_id}", response_model=ArtistRead)
def update_artist(
    artist_id: int,
    payload: ArtistUpdate,
    service: ArtistService = Depends(get_artist_service),
):
    return service.update_artist(artist_id, payload)


@router.delete("/{artist_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_artist(artist_id: int, service: ArtistService = Depends(get_artist_service)):
    service.delete_artist(artist_id)


@router.get("/{artist_id}/albums", response_model=list[AlbumRead])
def list_albums_by_artist(
    artist_id: int,
    service: AlbumService = Depends(get_album_service),
):
    return service.get_albums_by_artist(artist_id)
