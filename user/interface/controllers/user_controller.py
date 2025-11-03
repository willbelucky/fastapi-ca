from fastapi import APIRouter, Depends
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide
from containers import Container
from user.domain.user import User
from user.application.user_service import UserService

router = APIRouter(prefix="/users")


class CreateUserBody(BaseModel):
    name: str
    email: str
    password: str


@router.post("", status_code=201)
@inject
def create_user(
    user: CreateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service]),
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
@inject
def update_user(
    user_id: str,
    update_data: UpdateUser,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    updated_user: User = user_service.update_user(
        user_id=user_id,
        name=update_data.name,
        password=update_data.password,
    )

    return updated_user

@router.get("")
@inject
def get_users(
    page: int = 1,
    items_per_page: int = 10,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    # 튜플 언패킹 시 타입 명시 방법 1: 개별 변수에 타입 힌트
    total_count: int
    users: list[User]
    total_count, users = user_service.get_users(page, items_per_page)

    return {
        "total_count": total_count,
        "page": page,
        "users": users,
    }

@router.delete("", status_code=204)
@inject
def delete_user(
    user_id: str,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    user_service.delete_user(user_id)

    return None