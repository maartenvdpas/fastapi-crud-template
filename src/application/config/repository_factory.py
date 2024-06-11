from domain.user.user_repository import UserRepository
from infrastucture.sqlalchemy.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository

def get_user_repository() -> UserRepository:
    return SQLAlchemyUserRepository()