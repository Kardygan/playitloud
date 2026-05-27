from sqlalchemy import select
from sqlalchemy.orm import Session

from playitloud.models import Artist


class ArtistRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, artist: Artist) -> None:
        self.session.add(artist)

    def get_by_id(self, artist_id: int) -> Artist | None:
        statement = select(Artist).where(Artist.id == artist_id)

        return self.session.scalar(statement)

    def get_all(self) -> list[Artist]:
        statement = select(Artist)

        return list(self.session.scalars(statement).all())

    def get_all_by_ids(self, artist_ids: list[int]) -> list[Artist]:
        statement = select(Artist).where(Artist.id.in_(artist_ids))

        return list(self.session.scalars(statement).all())

    def delete(self, artist: Artist) -> None:
        self.session.delete(artist)
