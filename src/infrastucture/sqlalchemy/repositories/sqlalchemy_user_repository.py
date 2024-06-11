from sqlalchemy import select

from application.config.object_storage_factory import object_storage_factory
from domain.stored_object.stored_object import StoredObject
from domain.users.user_repository import UserRepository
from domain.users.user import User
from infrastucture.persistence.sqlalchemy.sqlalchemy import Session
from infrastucture.persistence.sqlalchemy.entities.user import User as UserEntity
from infrastucture.persistence.sqlalchemy.entities.stored_object import StoredObject as StoredObjectEntity
from infrastucture.persistence.sqlalchemy.repositories.stored_object_repository import SQLAlchemyStoredObjectRepository

class SQLAlchemyUserRepository(UserRepository):
    """
    A SQLAlchemy implementation of the UserRepository.
    """

    def create_user(self, user: User) -> None:
        db_user = UserEntity(password_hash=user.password_hash, user_name=user.user_handle)
        with Session.begin() as session:
            session.add(db_user)
            session.commit()

    def get_users(self, offset: int = 0, limit: int = 10) -> list[User]:
        query = select(UserEntity).offset(offset).limit(limit)
        with Session.begin() as session:
            query_result = session.scalars(query).all()
            return [SQLAlchemyUserRepository._construct_domain_object(u) for u in query_result]
        
        

    def get_user(self, user_handle: str) -> User:
        query = select(UserEntity).where(UserEntity.user_name == user_handle)

        with Session.begin() as session:
            query_result = session.scalars(query).one_or_none()
            return None if query_result == None else SQLAlchemyUserRepository._construct_domain_object(query_result)    


    def update_user(self, user: User) -> None:
        user_query = select(UserEntity).where(UserEntity.user_name == user.user_handle)

        with Session.begin() as session:
            db_user = session.scalars(user_query).one_or_none()
            db_user.about_me = user.about_me
            db_user.full_name = user.full_name
            #TODO - Add more fields as required or create some looper function to do this automatically
            session.commit()

    def update_user_avatar(self, user: User, avatar: StoredObject) -> None:
        user_query = select(UserEntity).where(UserEntity.user_name == user.user_handle)

        with Session.begin() as session:
            db_user = session.scalars(user_query).one_or_none()
            db_user.avatar = StoredObjectEntity(filename=avatar.filename, bucket=avatar.bucket)
            session.commit()

    def get_user_avatar(self, user: User) -> StoredObject:
        user_query = select(UserEntity).where(UserEntity.user_name == user.user_handle)

        with Session.begin() as session:
            db_user = session.scalars(user_query).one_or_none()
            return None if db_user == None else StoredObject(filename=db_user.avatar.filename, bucket=db_user.avatar.bucket)    

    
    def _construct_domain_object(db_user: UserEntity) -> User:
        avatar = SQLAlchemyStoredObjectRepository._construct_domain_object(db_user.avatar) if db_user else None
        return User(
            id=db_user.id,
            full_name=db_user.full_name,
            password_hash=db_user.password_hash,
            registered_at=db_user.registered_at,
            user_handle=db_user.user_name,
            about_me=db_user.about_me,
            talks_about=[],
            avatar=avatar
        )