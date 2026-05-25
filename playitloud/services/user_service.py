from sqlalchemy.orm import Session

from playitloud.models import User
from playitloud.repositories.user_repository import UserRepository
from playitloud.core.security import hash_password, verify_password
from playitloud.schemas.user import UserCreate, UserRead, UserUpdateInfo

class UserService:
    def __init__(self, session: Session, user_repository: UserRepository) -> None:
        self.session = session
        self.user_repository = user_repository  

    def create_user(self, user_create: UserCreate) -> UserRead:
        existing_user = self.user_repository.get_by_email(user_create.email)

        if existing_user:
            raise ValueError("Email already exists.")

        user = User(
            email=user_create.email,
            hashed_password=hash_password(user_create.password),
            first_name=user_create.first_name,
            last_name=user_create.last_name,
        )

        self.user_repository.add(user)
        self.session.commit()
        self.session.refresh(user)

        return UserRead.model_validate(user)
    
    def login_user(self, email: str, password: str) -> UserRead:
        user = self.user_repository.get_by_email(email)

        if not user:
            raise ValueError("Invalid email or password.")

        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password.")

        return UserRead.model_validate(user)

    def get_user_by_id(self, user_id: int) -> UserRead:
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise ValueError("User not found.")

        return UserRead.model_validate(user)
    
    def get_user_by_email(self, email: str) -> UserRead:
        user = self.user_repository.get_by_email(email)

        if not user:
            raise ValueError("User not found.")

        return UserRead.model_validate(user)

    def get_all_users(self) -> list[UserRead]:
        users = self.user_repository.get_all()
        
        return [UserRead.model_validate(user) for user in users]
    
    def update_user_info(self, user_id: int, user_update: UserUpdateInfo) -> UserRead:
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise ValueError("User not found.")

        user.first_name = user_update.first_name
        user.last_name = user_update.last_name

        self.session.commit()
        self.session.refresh(user)

        return UserRead.model_validate(user)

    def delete_user(self, user_id: int) -> None:
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise ValueError("User not found.")

        self.user_repository.soft_delete(user)
        self.session.commit()