import jwt
from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import Depends, Cookie
from secrets import token_hex
from jwt import InvalidTokenError

from application.auth.auth_token import AuthToken
from application.config.config import get_config
from application.config.repository_factory import user_repository, revoked_token_repository
from domain.user.user import User
from domain.user.user_repository import UserRepository


class AuthService():
    def __init__(
            self, 
            user_repository: UserRepository = Depends(user_repository), 
        ):
        self.user_repository = user_repository

    def create_session_token(self, user: User) -> str:
      
        subject_identity = user.get_identity()
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=get_config().TOKEN_TTL_MINUTES)
        
        token = AuthToken(
            id=token_hex(32),
            exp=expires_at,
            sub=subject_identity
        )

        return jwt.encode(token.model_dump(), get_config().SECRET_KEY, get_config().ALGORITHM), expires_at

    def get_session_token(self, session: Annotated[str, Cookie()]) -> AuthToken | None:
        try:
            payload = jwt.decode(session, get_config().SECRET_KEY, algorithms=[get_config().ALGORITHM])
        except InvalidTokenError as e:
            print(e)
            return None

        return AuthToken.model_validate(payload)

    def get_session_user(self, session: Annotated[str, Cookie()]) -> User | None:
        token = self.get_session_token(session)

        if token is None:
            return None

        return self.user_repository.get_user(token.sub)
        

async def get_session_user(session: Annotated[str | None, Cookie()] = None, auth_service: AuthService = Depends(AuthService)) -> User | None:
    if session is None:
        return None
    
    return auth_service.get_session_user(session)

async def get_session_token(session: Annotated[str | None, Cookie()] = None, auth_service: AuthService = Depends(AuthService)) -> User | None:
    if session is None:
        return None
    
    return auth_service.get_session_token(session)