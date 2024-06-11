from pydantic import BaseModel, EmailStr
from datetime import datetime

class User(BaseModel):
    """
    Representation of a user within the system. 
    """

    id: int = 0
    email: EmailStr
    password_hash: str | None = None
    registered_at: datetime

    def get_identity(self) -> str:
        """
        Returns the identity of the user, represented as a string. 

        This is currently the email address associated with the user. But this could
        be any uniquely identifying property of the user.
        """
        return self.email