from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from application.config.config import get_config

engine = create_engine(
    str(get_config().DATABASE_URL),
    future=True, #This enabled 'future 2.0 mode'
    echo=get_config().DATABASE_LOGGING
)

Session = sessionmaker(autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass