import pytest
from decimal import Decimal
from typing import Any

from pydantic import ValidationError


from playitloud.models.album import MediaType
from playitloud.repositories.album_repository import AlbumRepository
from playitloud.repositories.artist_repository import ArtistRepository
from playitloud.schemas.album import AlbumCreate, AlbumUpdate
from playitloud.schemas.artist import ArtistCreate
from playitloud.services.album_service import AlbumService
from playitloud.services.artist_service import ArtistService


def _make_album_service(db_session) -> AlbumService:
    return AlbumService(
        session=db_session,
        album_repository=AlbumRepository(db_session),
        artist_repository=ArtistRepository(db_session),
    )


def _make_artist(db_session, name: str = "Test Artist"):
    service = ArtistService(session=db_session, artist_repository=ArtistRepository(db_session))

    return service.create_artist(ArtistCreate(name=name))


def _album_create(**kwargs) -> AlbumCreate:
    defaults: dict[str, Any] = dict(name="Test Album", media_type=MediaType.CD, price=Decimal("14.99"), stock=5)
    defaults.update(kwargs)

    return AlbumCreate(**defaults)


def test_create_album_with_artists(db_session):
    service = _make_album_service(db_session)

    artist = _make_artist(db_session)

    result = service.create_album(_album_create(artist_ids=[artist.id]))

    assert len(result.artists) == 1
    assert result.artists[0].id == artist.id

    # price beyond 2 decimal places is rejected, not silently rounded to 10.00
    with pytest.raises(ValidationError):
        _album_create(price=Decimal("9.999"))


def test_create_album_invalid_artist_id(db_session):
    service = _make_album_service(db_session)

    with pytest.raises(ValueError, match="not found"):
        service.create_album(_album_create(artist_ids=[999]))


def test_update_album_replaces_artists(db_session):
    service = _make_album_service(db_session)

    artist_a = _make_artist(db_session, "Artist A")
    artist_b = _make_artist(db_session, "Artist B")

    created = service.create_album(_album_create(artist_ids=[artist_a.id]))

    updated = service.update_album(created.id, AlbumUpdate(
        name=created.name,
        price=created.price,
        stock=created.stock,
        artist_ids=[artist_b.id],
    ))

    assert len(updated.artists) == 1
    assert updated.artists[0].id == artist_b.id
