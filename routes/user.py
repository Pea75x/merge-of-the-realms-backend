from fastapi import HTTPException, Depends, APIRouter
from constants import *
from sqlalchemy.orm import Session
from models.user import User
from database import get_db
from auth import *
from schemas.user import *

router = APIRouter()

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    # Depends = automatically run function and inject return value into route
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    if user.role not in ALLOWED_ROLES:
        raise HTTPException(status_code=400, detail="Invalid role")
    if user.title not in ALLOWED_TITLES:
        raise HTTPException(status_code=400, detail="Invalid title")
    if user.weapons:
        if len(user.weapons) > 3:
            raise HTTPException(status_code=400, detail="Cannot have more than 3 weapons")
        if any(weapon not in ALLOWED_WEAPONS for weapon in user.weapons):
            raise HTTPException(status_code=400, detail="Some weapons are invalid")

    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role,
        title=user.title,
        weapons=user.weapons,
        avatar=user.avatar
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "msg": "User registered",
        "user_id": new_user.id
    }

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user or not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": user.email})
    return {"access_token": token, "user": existing_user}
