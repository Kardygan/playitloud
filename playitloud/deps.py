from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from playitloud.core.database import SessionLocal
from playitloud.repositories import (
    AddressRepository,
    AlbumRepository,
    ArtistRepository,
    OrderRepository,
    SupplierOfferRepository,
    SupplierOrderRepository,
    SupplierRepository,
    UserRepository,
)
from playitloud.services import (
    AddressService,
    AlbumService,
    ArtistService,
    OrderService,
    SupplierOfferService,
    SupplierOrderService,
    SupplierService,
    UserService,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_service(session: Session = Depends(get_db)) -> UserService:
    repository = UserRepository(session)
    return UserService(session=session, user_repository=repository)


def get_artist_service(session: Session = Depends(get_db)) -> ArtistService:
    return ArtistService(session=session, artist_repository=ArtistRepository(session))


def get_album_service(session: Session = Depends(get_db)) -> AlbumService:
    return AlbumService(
        session=session,
        album_repository=AlbumRepository(session),
        artist_repository=ArtistRepository(session),
    )


def get_address_service(session: Session = Depends(get_db)) -> AddressService:
    address_repository = AddressRepository(session)
    user_repository = UserRepository(session)
    return AddressService(
        session=session,
        address_repository=address_repository,
        user_repository=user_repository,
    )


def get_order_service(session: Session = Depends(get_db)) -> OrderService:
    return OrderService(
        session=session,
        order_repository=OrderRepository(session),
        user_repository=UserRepository(session),
        address_repository=AddressRepository(session),
        album_repository=AlbumRepository(session),
    )


def get_supplier_service(session: Session = Depends(get_db)) -> SupplierService:
    return SupplierService(session=session, supplier_repository=SupplierRepository(session))


def get_supplier_offer_service(session: Session = Depends(get_db)) -> SupplierOfferService:
    return SupplierOfferService(
        session=session,
        supplier_offer_repository=SupplierOfferRepository(session),
        supplier_repository=SupplierRepository(session),
        album_repository=AlbumRepository(session),
    )


def get_supplier_order_service(session: Session = Depends(get_db)) -> SupplierOrderService:
    return SupplierOrderService(
        session=session,
        supplier_order_repository=SupplierOrderRepository(session),
        supplier_repository=SupplierRepository(session),
        album_repository=AlbumRepository(session),
        supplier_offer_repository=SupplierOfferRepository(session),
    )
