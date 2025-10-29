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