from fastapi import APIRouter, Depends, Response, status

from playitloud.deps import get_album_service
from playitloud.schemas.album import AlbumCreate, AlbumRead, AlbumUpdate
from playitloud.services.album_service import AlbumService

router = APIRouter(prefix="/albums", tags=["albums"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=AlbumRead)
def create_album(
    payload: AlbumCreate,
    response: Response,
    service: AlbumService = Depends(get_album_service),
):
    album = service.create_album(payload)
    response.headers["Location"] = f"/albums/{album.id}"
    
    return album


@router.get("", response_model=list[AlbumRead])
def list_albums(service: AlbumService = Depends(get_album_service)):
    return service.get_all_albums()


@router.get("/{album_id}", response_model=AlbumRead)
def get_album(album_id: int, service: AlbumService = Depends(get_album_service)):
    return service.get_album_by_id(album_id)


@router.patch("/{album_id}", response_model=AlbumRead)
def update_album(
    album_id: int,
    payload: AlbumUpdate,
    service: AlbumService = Depends(get_album_service),
):
    return service.update_album(album_id, payload)


@router.delete("/{album_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_album(album_id: int, service: AlbumService = Depends(get_album_service)):
    service.delete_album(album_id)
