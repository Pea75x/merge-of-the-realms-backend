from pydantic import BaseModel

class CreateUserGroup(BaseModel):
  user_email: str
  group_id: int

class UserStatusUpdate(BaseModel):
  status: str
