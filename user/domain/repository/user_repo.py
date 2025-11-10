from abc import ABC, abstractmethod

from user.domain.user import User


class IUserRepository(ABC):
    @abstractmethod
    def save(self, user: User):
        raise NotImplementedError

    @abstractmethod
    def find_by_email(self, email: str) -> User:
        """
        Find a user by email.
        If not found, raise HTTPException(status_code=422, detail="User not found").
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_users(self, page: int, items_per_page: int) -> tuple[int, list[User]]:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str) -> None:
        raise NotImplementedError
