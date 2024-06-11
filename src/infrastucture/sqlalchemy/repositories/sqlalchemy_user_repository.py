from sqlalchemy import select

from domain.user.user_repository import UserRepository
from domain.user.user import User
from infrastucture.sqlalchemy.sqlalchemy import Session
from infrastucture.sqlalchemy.entities.user import UserEntity
from infrastucture.sqlalchemy.entities.transformers import user_transformer


class SQLAlchemyUserRepository(UserRepository):
    """
    A SQLAlchemy implementation of the UserRepository.
    """

    def create_user(self, user: User) -> None:
        db_user = user_transformer.to_entity(user)
        with Session.begin() as session:
            session.add(db_user)
            session.commit()
        
    def get_user_by_email(self, email: str) -> User:
        query = select(UserEntity).where(UserEntity.email == email)

        with Session.begin() as session:
            query_result = session.scalars(query).one_or_none()
            return None if query_result == None else user_transformer.to_domain_model(query_result)    