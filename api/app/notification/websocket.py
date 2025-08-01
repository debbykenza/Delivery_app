from fastapi import WebSocket, WebSocketDisconnect, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Optional
import json
from datetime import datetime

from app.services import websocket_manager

from ..core.config import settings
from ..core.security import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user_ws(
    websocket: WebSocket,
    token: Optional[str] = None
):
    if token is None:
        await websocket.close(code=1008)  # Policy Violation
        return None

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            await websocket.close(code=1008)
            return None
    except JWTError:
        await websocket.close(code=1008)
        return None

    return user_id

async def websocket_endpoint(websocket: WebSocket, token: str = None):
    user_id = await get_current_user_ws(websocket, token)
    if user_id is None:
        return

    await websocket_manager.connect(websocket, user_id)
    
    try:
        while True:
            # On peut recevoir des messages du client si nécessaire
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                # Traiter les messages entrants si besoin
            except json.JSONDecodeError:
                pass
            
    except WebSocketDisconnect:
        await websocket_manager.disconnect(websocket, user_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket_manager.disconnect(websocket, user_id)