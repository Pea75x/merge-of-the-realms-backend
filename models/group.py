from sqlalchemy import Column, Integer, String
from database import Base

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    problem = Column(String)
    total_time = Column(Integer, nullable=True)
    time_left = Column(Integer, nullable=True)
    game_status = Column(String, default="assembling_players", nullable=False)
    submission_time_allocated = Column(Integer, nullable=True)
    submission_time_taken = Column(Integer, nullable=True)
    build_time_allocated = Column(Integer, nullable=True)
    build_time_taken = Column(Integer, nullable=True)
    testing_time_allocated = Column(Integer, nullable=True)
    testing_tme_taken = Column(Integer, nullable=True)
