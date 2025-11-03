from ulid import ULID
from datetime import datetime
from fastapi import HTTPException
from utils.crypto import Crypto

from user.domain.user import User
from user.domain.repository.user_repo import IUserRepository


class UserService:
    def __init__(
        self,
        user_repo: IUserRepository
    ):
        self.user_repo = user_repo
        self.ulid = ULID()
        self.crypto = Crypto()

    def create_user(
        self,
        name: str,
        email: str,
        password: str,
        memo: str | None = None,
    ) -> User:
        _user = None

        try:
            _user = self.user_repo.find_by_email(email)
        except Exception as e:
            if e.status_code != 422:
                raise e

        if _user:
            raise HTTPException(status_code=422, detail="User already exists")

        now = datetime.now()
        user: User = User(
            id=self.ulid.generate(),
            name=name,
            email=email,
            password=self.crypto.encrypt(password),
            memo=memo,
            created_at=now,
            updated_at=now
        )
        self.user_repo.save(user)

        return user

    def update_user(
        self,
        user_id: str,
        name: str | None = None,
        password: str | None = None,
    ) -> User:
        user = self.user_repo.find_by_id(user_id)

        if name:
            user.name = name
        if password:
            user.password = self.crypto.encrypt(password)
        user.updated_at = datetime.now()

        self.user_repo.update(user)

        return user
