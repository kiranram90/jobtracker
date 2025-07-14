from pydantic import BaseModel

class UserDTO(BaseModel):
    email: str
    password: str
    