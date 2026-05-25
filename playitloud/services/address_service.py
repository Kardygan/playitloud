from sqlalchemy.orm import Session

from playitloud.models import Address
from playitloud.repositories.address_repository import AddressRepository
from playitloud.repositories.user_repository import UserRepository
from playitloud.schemas.address import AddressCreate, AddressRead, AddressUpdate


class AddressService:
    def __init__(
        self,
        session: Session,
        address_repository: AddressRepository,
        user_repository: UserRepository,
    ) -> None:
        self.session = session
        self.address_repository = address_repository
        self.user_repository = user_repository

    def create_address(self, user_id: int, address_create: AddressCreate) -> AddressRead:
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise ValueError("User not found.")

        address = Address(
            user_id=user_id,
            street=address_create.street,
            city=address_create.city,
            postal_code=address_create.postal_code,
            country_code=address_create.country_code,
        )

        self.address_repository.add(address)
        self.session.commit()
        self.session.refresh(address)

        return AddressRead.model_validate(address)

    def get_address(self, user_id: int, address_id: int) -> AddressRead:
        address = self.address_repository.get_by_id_and_user_id(address_id, user_id)

        if not address:
            raise ValueError("Address not found.")

        return AddressRead.model_validate(address)

    def get_user_addresses(self, user_id: int) -> list[AddressRead]:
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise ValueError("User not found.")

        addresses = self.address_repository.get_all_by_user_id(user_id)

        return [AddressRead.model_validate(a) for a in addresses]

    def update_address(
        self, user_id: int, address_id: int, address_update: AddressUpdate
    ) -> AddressRead:
        address = self.address_repository.get_by_id_and_user_id(address_id, user_id)

        if not address:
            raise ValueError("Address not found.")

        address.street = address_update.street
        address.city = address_update.city
        address.postal_code = address_update.postal_code
        address.country_code = address_update.country_code

        self.session.commit()
        self.session.refresh(address)

        return AddressRead.model_validate(address)

    def delete_address(self, user_id: int, address_id: int) -> None:
        address = self.address_repository.get_by_id_and_user_id(address_id, user_id)

        if not address:
            raise ValueError("Address not found.")

        self.address_repository.delete(address)
        self.session.commit()
