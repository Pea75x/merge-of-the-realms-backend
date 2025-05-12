from database import engine, Base  
from models.user import User
from models.group import Group
from models.user_group import UserGroup


Base.metadata.create_all(bind=engine)

print("Tables created successfully!")