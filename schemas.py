from enum import Enum
from pydantic import BaseModel, Field

class Role(str, Enum):
    VISITER: str = "visiter"
    USER: str = "user"
    MODERATER: str = "moderater"
    ADMIN: str = "admin"


class UserLogin(BaseModel):
    username: str
    password: str
    
class UserSys(UserLogin):
    role: Role = Field(default=Role.VISITER)
    hashpassword: str

class UserDB(UserLogin):
    id: int

class Post(BaseModel):
    text: str

class UserPost(Post):
    id: int
    username: str
    role: Role
