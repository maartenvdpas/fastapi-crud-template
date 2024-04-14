import os
from functools import lru_cache

class Config():
    def __init__(self):
        # Examples
        # self.SECRET_KEY = os.getenv('SECRET_KEY')
        # self.ALGORITHM = os.getenv('ALGORITHM')
        # self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
        pass

@lru_cache
def get_config():
    return Config()