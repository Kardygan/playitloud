from fastapi import APIRouter, Depends, Response, status

from playitloud.deps import get_user_service
from playitloud.schemas import UserCreate, UserRead, UserUpdateInfo
from playitloud.services import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserRead)
def create_user(payload: UserCreate, response: Response, service: UserService = Depends(get_user_service)):
    user = service.create_user(payload)
    response.headers["Location"] = f"/users/{user.id}"
    return user


@router.get("", response_model=list[UserRead])
def list_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    return service.get_user_by_id(user_id)


@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, payload: UserUpdateInfo, service: UserService = Depends(get_user_service)):
    return service.update_user_info(user_id, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    service.delete_user(user_id)
