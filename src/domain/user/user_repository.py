from abc import ABC, abstractmethod
from pydantic import EmailStr
from domain.user.user import User

class UserRepository(ABC):
    @abstractmethod
    def get_user_by_email(self, email: EmailStr) -> User:
        pass

    @abstractmethod
    def create_user(self, user: User) -> None:
        pass