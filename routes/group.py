from fastapi import HTTPException, Depends, APIRouter
from constants import *
from sqlalchemy.orm import Session
from models.group import Group
from models.user_group import UserGroup
from database import get_db
from auth import *
from schemas.group import *

router = APIRouter()

@router.post("/create-group")
def create_group(group: CreateGroup, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_group = Group(
        name=group.name,
        problem=group.problem,
        total_time=group.total_time,
        submission_time_allocated=group.submission_time_allocated,
        build_time_allocated=group.build_time_allocated,
        testing_time_allocated=group.testing_time_allocated
    )

    db.add(new_group)
    db.commit()
    db.refresh(new_group)

    association = UserGroup(
        user_id=current_user.id,
        group_id=new_group.id,
        status="active"
    )

    db.add(association)
    db.commit()

    return {
        "msg": "Group created",
        "group_id": new_group.id
    }
