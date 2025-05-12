from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    role: str
    title: str
    weapons: list[str]
    avatar: str
    email: EmailStr
    
#class defines and validates the structure of incoming user data
class UserLogin(BaseModel):
    email: str
    password: str