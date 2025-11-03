from fastapi import APIRouter, Depends
from pydantic import BaseModel

from containers import get_user_service
from user.domain.user import User
from user.application.user_service import UserService

router = APIRouter(prefix="/users")


class CreateUserBody(BaseModel):
    name: str
    email: str
    password: str


@router.post("", status_code=201)
def create_user(
    user: CreateUserBody,
    user_service: UserService = Depends(get_user_service),
):
    created_user: User = user_service.create_user(
        name=user.name,
        email=user.email,
        password=user.password,
    )

    return created_user

class UpdateUser(BaseModel):
    name: str | None = None
    password: str | None = None

@router.put("/{user_id}")
def update_user(
    user_id: str,
    updated_user: UpdateUser,
    user_service: UserService = Depends(get_user_service),
):
    updated_user: User = user_service.update_user(
        user_id=user_id,
        name=updated_user.name,
        password=updated_user.password,
    )

    return updated_user