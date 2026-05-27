from decimal import Decimal

from playitloud.models import Album, Artist
from playitloud.models.album import MediaType
from playitloud.repositories.album_repository import AlbumRepository


def _make_artist(session, name: str = "Test Artist") -> Artist:
    artist = Artist(name=name)

    session.add(artist)
    session.commit()

    return artist


def _make_album(session, name: str = "Test Album", artist: Artist | None = None) -> Album:
    album = Album(name=name, media_type=MediaType.CD, price=Decimal("14.99"), stock=10)

    if artist:
        album.artists = [artist]

    session.add(album)
    session.commit()

    return album


def test_add_and_get_by_id(db_session):
    repo = AlbumRepository(db_session)

    artist = _make_artist(db_session)
    album = _make_album(db_session, artist=artist)

    fetched = repo.get_by_id(album.id)

    assert fetched is not None
    assert fetched.name == "Test Album"
    assert len(fetched.artists) == 1
    assert fetched.artists[0].name == "Test Artist"


def test_get_all_by_artist_id(db_session):
    repo = AlbumRepository(db_session)

    artist = _make_artist(db_session)
    _make_album(db_session, name="Album A", artist=artist)
    _make_album(db_session, name="Album B", artist=artist)
    _make_album(db_session, name="Album C")

    albums = repo.get_all_by_artist_id(artist.id)

    assert len(albums) == 2


def test_delete(db_session):
    repo = AlbumRepository(db_session)

    album = _make_album(db_session)

    repo.delete(album)
    db_session.commit()

    assert repo.get_by_id(album.id) is None
