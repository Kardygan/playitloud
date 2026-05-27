from playitloud.models import Artist
from playitloud.repositories.artist_repository import ArtistRepository


def test_add_and_get_by_id(db_session):
    repo = ArtistRepository(db_session)

    artist = Artist(name="Pink Floyd", description="Psychedelic rock band")

    repo.add(artist)
    db_session.commit()

    fetched = repo.get_by_id(artist.id)

    assert fetched is not None
    assert fetched.name == "Pink Floyd"
    assert fetched.description == "Psychedelic rock band"


def test_get_all_by_ids(db_session):
    repo = ArtistRepository(db_session)

    artist_a = Artist(name="Artist A")
    artist_b = Artist(name="Artist B")
    artist_c = Artist(name="Artist C")

    repo.add(artist_a)
    repo.add(artist_b)
    repo.add(artist_c)

    db_session.commit()

    result = repo.get_all_by_ids([artist_a.id, artist_c.id])

    assert len(result) == 2
    assert {a.name for a in result} == {"Artist A", "Artist C"}


def test_delete(db_session):
    repo = ArtistRepository(db_session)

    artist = Artist(name="To Delete")

    repo.add(artist)
    db_session.commit()

    repo.delete(artist)
    db_session.commit()

    assert repo.get_by_id(artist.id) is None
