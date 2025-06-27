from pydantic import BaseModel
from datetime import datetime


class UserDTO(BaseModel):
    email: str
    password: str
