import os
from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache

class Config(BaseSettings):
    """
    Load your configuration from the environment at load time as fields withing the object, 
    then provide the config via cache as it should be immutable at runtime.
    """

    APP_DIR: Path = Path(__file__).resolve().parent.parent

    STATIC_DIR: Path = APP_DIR / "web/static"
    TEMPLATE_DIR: Path = APP_DIR / "web/templates"
        
@lru_cache
def get_config():
    return Config()