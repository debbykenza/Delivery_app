# from fastapi import WebSocket
# from typing import Dict, List
# import json
# import asyncio

# class WebSocketManager:
#     def __init__(self):
#         self.active_connections: Dict[str, List[WebSocket]] = {}
#         self.lock = asyncio.Lock()

#     async def connect(self, websocket: WebSocket, user_id: str):
#         await websocket.accept()
#         async with self.lock:
#             if user_id not in self.active_connections:
#                 self.active_connections[user_id] = []
#             self.active_connections[user_id].append(websocket)

#     async def disconnect(self, websocket: WebSocket, user_id: str):
#         async with self.lock:
#             if user_id in self.active_connections:
#                 self.active_connections[user_id] = [
#                     ws for ws in self.active_connections[user_id] if ws != websocket
#                 ]
#                 if not self.active_connections[user_id]:
#                     del self.active_connections[user_id]

#     async def broadcast_to_user(self, user_id: str, message: dict):
#         async with self.lock:
#             if user_id in self.active_connections:
#                 disconnected = []
#                 for websocket in self.active_connections[user_id]:
#                     try:
#                         await websocket.send_text(json.dumps(message))
#                     except:
#                         disconnected.append(websocket)
                
#                 # Nettoyer les connexions déconnectées
#                 for ws in disconnected:
#                     await self.disconnect(ws, user_id)

# websocket_manager = WebSocketManager()

from fastapi import WebSocket
from typing import Dict, List
import json

class WebSocketManager:
    def __init__(self):
        # Dictionnaire pour stocker les connexions actives
        # Clé: user_id_user_type, Valeur: liste des WebSocket
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_key: str):
        """Accepte une nouvelle connexion WebSocket"""
        await websocket.accept()
        
        if user_key not in self.active_connections:
            self.active_connections[user_key] = []
        
        self.active_connections[user_key].append(websocket)
        print(f"Nouvelle connexion WebSocket pour {user_key}. Total: {len(self.active_connections[user_key])}")

    async def disconnect(self, websocket: WebSocket, user_key: str):
        """Supprime une connexion WebSocket"""
        if user_key in self.active_connections:
            try:
                self.active_connections[user_key].remove(websocket)
                if not self.active_connections[user_key]:
                    del self.active_connections[user_key]
                print(f"Connexion WebSocket fermée pour {user_key}")
            except ValueError:
                # La connexion n'était pas dans la liste
                pass

    async def send_personal_message(self, message: str, user_key: str):
        """Envoie un message à un utilisateur spécifique"""
        if user_key in self.active_connections:
            # Créer une copie de la liste pour éviter les modifications pendant l'itération
            connections = self.active_connections[user_key].copy()
            
            for websocket in connections:
                try:
                    await websocket.send_text(message)
                except Exception as e:
                    print(f"Erreur lors de l'envoi du message à {user_key}: {e}")
                    # Supprimer la connexion défaillante
                    await self.disconnect(websocket, user_key)

    async def broadcast(self, message: str):
        """Diffuse un message à toutes les connexions actives"""
        for user_key, connections in self.active_connections.items():
            connections_copy = connections.copy()
            for websocket in connections_copy:
                try:
                    await websocket.send_text(message)
                except Exception as e:
                    print(f"Erreur lors de la diffusion à {user_key}: {e}")
                    await self.disconnect(websocket, user_key)

    def get_connection_count(self) -> int:
        """Retourne le nombre total de connexions actives"""
        return sum(len(connections) for connections in self.active_connections.values())

    def get_user_connection_count(self, user_key: str) -> int:
        """Retourne le nombre de connexions pour un utilisateur spécifique"""
        return len(self.active_connections.get(user_key, []))

    def is_user_connected(self, user_key: str) -> bool:
        """Vérifie si un utilisateur a au moins une connexion active"""
        return user_key in self.active_connections and len(self.active_connections[user_key]) > 0

# Instance globale du gestionnaire
websocket_manager = WebSocketManager()