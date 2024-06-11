from domain.user.user import User
from infrastucture.sqlalchemy.entities.user import UserEntity

def to_domain_model(entity: UserEntity):
    return User(
            id=entity.id,
            email=entity.email,
            password_hash=entity.password_hash,
            registered_at=entity.registered_at
        )


def to_entity(domain_object: User):
    return UserEntity(
        id=domain_object.id,
        email=domain_object.email,
        password_hash=domain_object.password_hash,
        registered_at=domain_object.registered_at
    )