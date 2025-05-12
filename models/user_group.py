from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from database import Base

class UserGroup(Base):
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"))
    status = Column(String, default="invited", nullable=False)

    user = relationship("User", back_populates="user_groups")
