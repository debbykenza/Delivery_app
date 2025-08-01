from fastapi import WebSocket
from typing import Dict, List
import json
import asyncio

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        async with self.lock:
            if user_id not in self.active_connections:
                self.active_connections[user_id] = []
            self.active_connections[user_id].append(websocket)

    async def disconnect(self, websocket: WebSocket, user_id: str):
        async with self.lock:
            if user_id in self.active_connections:
                self.active_connections[user_id] = [
                    ws for ws in self.active_connections[user_id] if ws != websocket
                ]
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]

    async def broadcast_to_user(self, user_id: str, message: dict):
        async with self.lock:
            if user_id in self.active_connections:
                disconnected = []
                for websocket in self.active_connections[user_id]:
                    try:
                        await websocket.send_text(json.dumps(message))
                    except:
                        disconnected.append(websocket)
                
                # Nettoyer les connexions déconnectées
                for ws in disconnected:
                    await self.disconnect(ws, user_id)

websocket_manager = WebSocketManager()