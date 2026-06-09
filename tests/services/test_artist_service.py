import pytest

from playitloud.core.constants import DEFAULT_IMAGE_URL
from playitloud.repositories.artist_repository import ArtistRepository
from playitloud.schemas.artist import ArtistCreate, ArtistUpdate
from playitloud.services.artist_service import ArtistService


def _make_service(db_session) -> ArtistService:
    return ArtistService(session=db_session, artist_repository=ArtistRepository(db_session))


def test_create_artist(db_session):
    service = _make_service(db_session)

    result = service.create_artist(ArtistCreate(name="Pink Floyd"))

    assert result.id is not None
    assert result.name == "Pink Floyd"
    # no picture set -> falls back to the default image
    assert result.picture_url == DEFAULT_IMAGE_URL


def test_update_artist(db_session):
    service = _make_service(db_session)

    created = service.create_artist(ArtistCreate(name="Old Name"))
    updated = service.update_artist(created.id, ArtistUpdate(name="New Name", description="Updated"))

    assert updated.name == "New Name"
    assert updated.description == "Updated"


def test_delete_artist(db_session):
    service = _make_service(db_session)

    created = service.create_artist(ArtistCreate(name="To Delete"))
    service.delete_artist(created.id)

    with pytest.raises(ValueError, match="not found"):
        service.get_artist_by_id(created.id)
