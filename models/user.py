from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
    title = Column(String)
    weapons = Column(ARRAY(String))
    avatar = Column(String)

    user_groups = relationship("UserGroup", back_populates="user")
