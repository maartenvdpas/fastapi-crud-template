from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class AuthToken(BaseModel):
    """
    Representation of a user within the system. 
    """

    id: str
    exp: datetime
    sub: str