from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING
from playitloud.models.base import Base

if TYPE_CHECKING:
    from playitloud.models.user import User

class Address(Base):
    __tablename__ = "addresses"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    
    street: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    
    postal_code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    
    country_code: Mapped[str] = mapped_column(
        String(2),
        nullable=False,
    )
    
    user: Mapped["User"] = relationship(
        back_populates="addresses",
    )