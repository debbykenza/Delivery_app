from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.models.notification import Notification, TypeNotification
from app.schemas.notification import NotificationCreate
from fastapi import WebSocket, WebSocketDisconnect
import json
from app.services.websocket_manager import websocket_manager

# def lire_notifications(db: Session, user_id: UUID, user_type: str, seulement_non_lues: bool = False) -> List[Notification]:
#     query = db.query(Notification).filter(
#         Notification.user_id == user_id,
#         Notification.user_type == user_type
#     )
#     if seulement_non_lues:
#         query = query.filter(Notification.lu == False)
#     return query.order_by(Notification.date_envoi.desc()).all()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def lire_notifications(db: Session, user_id: UUID, user_type: str, seulement_non_lues: bool = False) -> List[Notification]:
    query = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.user_type == user_type
    )

    # ➤ filtre selon la valeur de seulement_non_lues
    query = query.filter(Notification.lu == (not seulement_non_lues))

    return query.order_by(Notification.date_envoi.desc()).all()


def creer_notification(db: Session, notif: NotificationCreate) -> Notification:
    db_notif = Notification(**notif.dict())
    db.add(db_notif)
    db.commit()
    db.refresh(db_notif)
    return db_notif

def marquer_comme_lue(db: Session, notif_id: UUID):
    notif = db.query(Notification).filter(Notification.id == notif_id).first()
    if notif:
        notif.lu = True
        db.commit()
    return notif


# async def get_current_user_ws(
#     websocket: WebSocket,
#     token: Optional[str] = None
# ):
#     if token is None:
#         await websocket.close(code=1008)  # Policy Violation
#         return None

#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         user_id: str = payload.get("sub")
#         if user_id is None:
#             await websocket.close(code=1008)
#             return None
#     except JWTError:
#         await websocket.close(code=1008)
#         return None

#     return user_id

async def websocket_endpoint(websocket: WebSocket, token: str = None):
    user_id = "None"
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
