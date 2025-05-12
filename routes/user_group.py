from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from database import get_db
from models.user_group import *
from models.user import User
from schemas.user_group import *
from collections import defaultdict
import json
from database import SessionLocal

router = APIRouter()

@router.post("/join-group")
def join_group(data: CreateUserGroup, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=data.user_email).first()
    if not user:
        raise HTTPException(status_code=400, detail="No user found")

    existing = db.query(UserGroup).filter_by(user_id=user.id, group_id=data.group_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already in group")
    
    association = UserGroup(
        user_id=user.id,
        group_id=data.group_id      
    )

    db.add(association)
    db.commit()
    db.refresh(association)
    broadcast_group_status(association.id, db)

    return {
        "msg": "User added to group",
        "user_group_id": association.id
    }

@router.put("/user-groups/{user_group_id}")
def update_user_group(
    user_group_id: int,
    status_data: UserStatusUpdate,
    db: Session = Depends(get_db)
):
    user_group = db.query(UserGroup).filter(UserGroup.id == user_group_id).first()
    if not user_group:
        raise HTTPException(status_code=404, detail="invite not found")

    user_group.status = status_data.status
    db.commit()
    db.refresh(user_group)
    broadcast_group_status(user_group.id, db)
    return {
        "msg": "UserGroup status updated",
        "new_status": user_group.status
    }

group_connections = defaultdict(set)


@router.websocket("/ws/quest-council/{group_id}")
async def quest_council_ws(websocket: WebSocket, group_id: int):
    await websocket.accept()
    db = SessionLocal() 
    try:
        group_connections[group_id].add(websocket)
        await broadcast_group_status(group_id, db)

        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        group_connections[group_id].remove(websocket)
        await broadcast_group_status(group_id, db)
    finally:
        db.close()


async def broadcast_group_status(group_id: int, db: Session):
    user_groups = db.query(UserGroup).filter_by(group_id=group_id).all()
    data = [
        {
            "user": {
                "id": invite.user.id,
                "name": invite.user.name,
                "email": invite.user.email,
                "avatar": invite.user.avatar
            },
            "status": invite.status
        }
        for invite in user_groups
    ]
    message = json.dumps({"group_id": group_id, "members": data})
    for ws in group_connections[group_id]:
        await ws.send_text(message)