# from fastapi import APIRouter, Depends, HTTPException, status, WebSocket
# from sqlalchemy.orm import Session
# from typing import List
# from uuid import UUID

# from app.schemas.notification import NotificationCreate, NotificationRead, NotificationUpdate
# from app.services.notification import lire_notifications as service_lire_notifications, creer_notification, marquer_comme_lue, websocket_endpoint
# from app.core.database import get_db

# router = APIRouter(prefix="/notifications", tags=["Notifications"])

# @router.get("/", response_model=List[NotificationRead])
# def lire_notifications(
#     user_id: UUID,
#     user_type: str,
#     non_lues: bool = False,
#     db: Session = Depends(get_db)
# ):
#     return service_lire_notifications(db, user_id=user_id, user_type=user_type, seulement_non_lues=non_lues)

# @router.post("/", response_model=NotificationRead, status_code=status.HTTP_201_CREATED)
# def ajouter_notification(notif: NotificationCreate, db: Session = Depends(get_db)):
#     return creer_notification(db, notif)

# @router.patch("/{notif_id}/lue", response_model=NotificationRead)
# def marquer_notification_comme_lue(notif_id: UUID, db: Session = Depends(get_db)):
#     notif = marquer_comme_lue(db, notif_id)
#     if not notif:
#         raise HTTPException(status_code=404, detail="Notification non trouvée")
#     return notif

# # commenté de base
# # @router.websocket("/ws")
# # async def websocket_endpoint(websocket: WebSocket):
# #     await websocket.accept()
# #     while True:
# #         data = await websocket.receive_text()
# #         await websocket.send_text(f"Message text was: {data}")

# @router.websocket("/ws")
# async def notifications_websocket(
#     websocket: WebSocket,
#     # token: str = None
# ):
#     await websocket_endpoint(websocket)
    
    
from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.schemas.notification import (
    NotificationCreate, 
    NotificationRead, 
    NotificationUpdate,
    TypeNotification
)
from app.services.notification import (
    lire_notifications_utilisateur,
    compter_notifications_non_lues,
    obtenir_statistiques_notifications,
    creer_notification,
    marquer_comme_lue,
    marquer_toutes_comme_lues,
    supprimer_notification,
    supprimer_notifications_lues,
    websocket_endpoint
)
from app.core.database import get_db
# from app.core.auth import get_current_user  # Décommentez si vous avez un système d'auth

router = APIRouter(prefix="/notifications", tags=["Notifications"])

# Endpoint pour récupérer les notifications d'un utilisateur
@router.get("/user/{user_id}", response_model=List[NotificationRead])
def lire_notifications_utilisateur_endpoint(
    user_id: UUID,
    user_type: str,
    non_lues: Optional[bool] = Query(False, description="Afficher seulement les notifications non lues"),
    type_notification: Optional[TypeNotification] = Query(None, description="Filtrer par type de notification"),
    limite: Optional[int] = Query(50, ge=1, le=100, description="Nombre maximum de notifications (1-100)"),
    depuis_jours: Optional[int] = Query(None, ge=1, le=365, description="Notifications depuis X jours"),
    db: Session = Depends(get_db)
):
    """
    Récupère les notifications pour un utilisateur spécifique
    
    - **user_id**: ID de l'utilisateur
    - **user_type**: Type d'utilisateur (client, marchand, livreur, admin)
    - **non_lues**: Si true, ne retourne que les notifications non lues
    - **type_notification**: Filtre par type (info, warning, error, success)
    - **limite**: Nombre maximum de notifications à retourner
    - **depuis_jours**: Ne retourner que les notifications des X derniers jours
    """
    depuis_date = None
    if depuis_jours:
        from datetime import timedelta
        depuis_date = datetime.utcnow() - timedelta(days=depuis_jours)
    
    notifications = lire_notifications_utilisateur(
        db=db,
        user_id=user_id,
        user_type=user_type,
        seulement_non_lues=non_lues,
        type_notification=type_notification,
        limite=limite,
        depuis_date=depuis_date
    )
    
    return notifications

# Endpoint pour compter les notifications non lues
@router.get("/user/{user_id}/count", response_model=dict)
def compter_notifications_non_lues_endpoint(
    user_id: UUID,
    user_type: str,
    db: Session = Depends(get_db)
):
    """
    Compte le nombre de notifications non lues pour un utilisateur
    """
    count = compter_notifications_non_lues(db, user_id, user_type)
    return {"user_id": user_id, "non_lues": count}

# Endpoint pour les statistiques des notifications
@router.get("/user/{user_id}/stats", response_model=dict)
def obtenir_statistiques_notifications_endpoint(
    user_id: UUID,
    user_type: str,
    db: Session = Depends(get_db)
):
    """
    Retourne des statistiques détaillées sur les notifications d'un utilisateur
    """
    stats = obtenir_statistiques_notifications(db, user_id, user_type)
    stats["user_id"] = str(user_id)
    stats["user_type"] = user_type
    return stats

# Endpoint pour créer une notification
@router.post("/", response_model=NotificationRead, status_code=status.HTTP_201_CREATED)
def creer_notification_endpoint(
    notif: NotificationCreate, 
    db: Session = Depends(get_db)
):
    """
    Crée une nouvelle notification
    """
    return creer_notification(db, notif)

# Endpoint pour marquer une notification comme lue
@router.patch("/{notif_id}/read", response_model=NotificationRead)
def marquer_notification_comme_lue_endpoint(
    notif_id: UUID,
    user_id: Optional[UUID] = Query(None, description="ID de l'utilisateur pour vérification"),
    db: Session = Depends(get_db)
):
    """
    Marque une notification comme lue
    """
    notif = marquer_comme_lue(db, notif_id, user_id)
    if not notif:
        raise HTTPException(
            status_code=404, 
            detail="Notification non trouvée ou vous n'avez pas l'autorisation"
        )
    return notif

# Endpoint pour marquer toutes les notifications comme lues
@router.patch("/user/{user_id}/read-all")
def marquer_toutes_comme_lues_endpoint(
    user_id: UUID,
    user_type: str,
    db: Session = Depends(get_db)
):
    """
    Marque toutes les notifications d'un utilisateur comme lues
    """
    count = marquer_toutes_comme_lues(db, user_id, user_type)
    return {
        "message": f"{count} notifications marquées comme lues",
        "count": count,
        "user_id": str(user_id)
    }

# Endpoint pour supprimer une notification
@router.delete("/{notif_id}")
def supprimer_notification_endpoint(
    notif_id: UUID,
    user_id: Optional[UUID] = Query(None, description="ID de l'utilisateur pour vérification"),
    db: Session = Depends(get_db)
):
    """
    Supprime une notification
    """
    success = supprimer_notification(db, notif_id, user_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Notification non trouvée ou vous n'avez pas l'autorisation"
        )
    return {"message": "Notification supprimée avec succès"}

# Endpoint pour supprimer toutes les notifications lues
@router.delete("/user/{user_id}/read")
def supprimer_notifications_lues_endpoint(
    user_id: UUID,
    user_type: str,
    db: Session = Depends(get_db)
):
    """
    Supprime toutes les notifications lues d'un utilisateur
    """
    count = supprimer_notifications_lues(db, user_id, user_type)
    return {
        "message": f"{count} notifications lues supprimées",
        "count": count,
        "user_id": str(user_id)
    }

# WebSocket pour notifications en temps réel
@router.websocket("/ws")
async def notifications_websocket(
    websocket: WebSocket,
    user_id: str = Query(..., description="ID de l'utilisateur"),
    user_type: str = Query(..., description="Type d'utilisateur")
):
    """
    WebSocket pour recevoir les notifications en temps réel
    
    Paramètres de query:
    - user_id: ID de l'utilisateur connecté
    - user_type: Type d'utilisateur (client, marchand, livreur, admin)
    """
    await websocket_endpoint(websocket, user_id, user_type)

# Endpoint legacy pour compatibilité (déprécié)
@router.get("/", response_model=List[NotificationRead])
def lire_notifications_legacy(
    user_id: UUID,
    user_type: str,
    non_lues: bool = False,
    db: Session = Depends(get_db)
):
    """
    [DÉPRÉCIÉ] Utilisez /user/{user_id} à la place
    """
    return lire_notifications_utilisateur(
        db=db,
        user_id=user_id,
        user_type=user_type,
        seulement_non_lues=non_lues
    )

# Endpoint pour marquer comme lue (legacy)
@router.patch("/{notif_id}/lue", response_model=NotificationRead)
def marquer_notification_comme_lue_legacy(
    notif_id: UUID, 
    db: Session = Depends(get_db)
):
    """
    [DÉPRÉCIÉ] Utilisez /{notif_id}/read à la place
    """
    notif = marquer_comme_lue(db, notif_id)
    if not notif:
        raise HTTPException(status_code=404, detail="Notification non trouvée")
    return notif