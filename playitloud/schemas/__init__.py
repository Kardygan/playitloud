from .address import (
    AddressCreate,
    AddressRead,
    AddressUpdate,
)
from .album import (
    AlbumCreate,
    AlbumRead,
    AlbumUpdate,
)
from .artist import (
    ArtistCreate,
    ArtistRead,
    ArtistUpdate,
)
from .user import (
    UserCreate,
    UserLogin,
    UserRead,
    UserUpdateInfo,
)

__all__ = [
    "AddressCreate",
    "AddressRead",
    "AddressUpdate",
    "AlbumCreate",
    "AlbumRead",
    "AlbumUpdate",
    "ArtistCreate",
    "ArtistRead",
    "ArtistUpdate",
    "UserCreate",
    "UserLogin",
    "UserRead",
    "UserUpdateInfo",
]