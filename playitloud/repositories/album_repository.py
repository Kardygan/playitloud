from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from playitloud.models import Album, Artist


class AlbumRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, album: Album) -> None:
        self.session.add(album)

    def get_by_id(self, album_id: int) -> Album | None:
        statement = select(Album).where(Album.id == album_id).options(selectinload(Album.artists))

        return self.session.scalar(statement)

    def get_all(self) -> list[Album]:
        statement = select(Album).options(selectinload(Album.artists))

        return list(self.session.scalars(statement).all())

    def get_all_by_artist_id(self, artist_id: int) -> list[Album]:
        statement = (
            select(Album)
            .join(Album.artists)
            .where(Artist.id == artist_id)
            .options(selectinload(Album.artists))
        )

        return list(self.session.scalars(statement).all())

    def delete(self, album: Album) -> None:
        self.session.delete(album)
