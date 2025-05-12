from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from database import *
import auth
import json
from routes import user, group, user_group


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# clients = {}

# async def broadcast_user_list():
#     message = json.dumps({
#         "users": list(clients.keys())
#     })
#     for client in clients.values():
#         await client.send_text(message)

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
#     token = token.replace("Bearer ", "")
#     user = auth.decode_jwt(token) 
#     username = user["sub"]
    
#     await websocket.accept()
#     clients[username] = websocket

#     await broadcast_user_list()

#     try:
#         while True:
#             data = await websocket.receive_text()
#             # handle incoming messages
#             message = json.dumps({
#                 "message": {
#                     "user": username,
#                     "data": data
#                 }
#             })
#             for client in clients.values():
#                 await client.send_text(message)
#     except WebSocketDisconnect:
#         clients.pop(username, None)
#         await broadcast_user_list()
#         return

# @app.websocket("/quest-council")

# async def quest_council(websocket: WebSocket, token: str = Query(...))
#     token = token.replace("Bearer ", "")
#     user = auth.decode_jwt(token) 
#     username = user["sub"]
    
#     await websocket.accept()
#     clients[username] = websocket

# /register
app.include_router(user.router)

# /users/register
# app.include_router(user.router, prefix="/users", tags=["Users"])

app.include_router(user_group.router)
app.include_router(group.router)