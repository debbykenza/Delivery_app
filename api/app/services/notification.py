from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
from datetime import datetime, timedelta

from app.models.notification import Notification, TypeNotification
from app.schemas.notification import NotificationCreate
from fastapi import WebSocket, WebSocketDisconnect, HTTPException
import json
from app.services.websocket_manager import websocket_manager

def lire_notifications_utilisateur(
    db: Session, 
    user_id: UUID, 
    user_type: str, 
    seulement_non_lues: bool = False,
    type_notification: Optional[TypeNotification] = None,
    limite: Optional[int] = None,
    depuis_date: Optional[datetime] = None
) -> List[Notification]:
    """
    Récupère les notifications pour un utilisateur spécifique avec des filtres optionnels
    
    Args:
        db: Session de base de données
        user_id: ID de l'utilisateur
        user_type: Type d'utilisateur (client, marchand, livreur, admin)
        seulement_non_lues: Si True, ne retourne que les notifications non lues
        type_notification: Filtre par type de notification (info, warning, error, success)
        limite: Nombre maximum de notifications à retourner
        depuis_date: Ne retourner que les notifications depuis cette date
    
    Returns:
        Liste des notifications
    """
    query = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.user_type == user_type
    )
    
    # Filtre par statut de lecture
    if seulement_non_lues:
        query = query.filter(Notification.lu == False)
    
    # Filtre par type de notification
    if type_notification:
        query = query.filter(Notification.type == type_notification)
    
    # Filtre par date
    if depuis_date:
        query = query.filter(Notification.date_envoi >= depuis_date)
    
    # Tri par date décroissante (plus récentes en premier)
    query = query.order_by(Notification.date_envoi.desc())
    
    # Limite le nombre de résultats
    if limite:
        query = query.limit(limite)
    
    return query.all()

def compter_notifications_non_lues(db: Session, user_id: UUID, user_type: str) -> int:
    """
    Compte le nombre de notifications non lues pour un utilisateur
    
    Args:
        db: Session de base de données
        user_id: ID de l'utilisateur
        user_type: Type d'utilisateur
    
    Returns:
        Nombre de notifications non lues
    """
    return db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.user_type == user_type,
        Notification.lu == False
    ).count()

def obtenir_statistiques_notifications(db: Session, user_id: UUID, user_type: str) -> dict:
    """
    Retourne des statistiques sur les notifications d'un utilisateur
    
    Args:
        db: Session de base de données
        user_id: ID de l'utilisateur
        user_type: Type d'utilisateur
    
    Returns:
        Dictionnaire avec les statistiques
    """
    base_query = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.user_type == user_type
    )
    
    total = base_query.count()
    non_lues = base_query.filter(Notification.lu == False).count()
    
    # Compter par type
    stats_par_type = {}
    for type_notif in TypeNotification:
        stats_par_type[type_notif.value] = base_query.filter(
            Notification.type == type_notif
        ).count()
    
    # Notifications récentes (dernières 24h)
    il_y_a_24h = datetime.utcnow() - timedelta(hours=24)
    recentes = base_query.filter(Notification.date_envoi >= il_y_a_24h).count()
    
    return {
        "total": total,
        "non_lues": non_lues,
        "lues": total - non_lues,
        "recentes_24h": recentes,
        "par_type": stats_par_type
    }

def creer_notification(db: Session, notif: NotificationCreate) -> Notification:
    """
    Crée une nouvelle notification
    
    Args:
        db: Session de base de données
        notif: Données de la notification à créer
    
    Returns:
        La notification créée
    """
    db_notif = Notification(**notif.dict())
    db.add(db_notif)
    db.commit()
    db.refresh(db_notif)
    
    # Envoyer la notification via WebSocket si l'utilisateur est connecté
    try:
        notification_data = {
            "id": str(db_notif.id),
            "titre": db_notif.titre,
            "message": db_notif.message,
            "type": db_notif.type.value,
            "date_envoi": db_notif.date_envoi.isoformat()
        }
        # Convertir l'UUID en string pour la clé
        user_key = f"{db_notif.user_id}_{db_notif.user_type}"
        websocket_manager.send_personal_message(json.dumps(notification_data), user_key)
    except Exception as e:
        print(f"Erreur lors de l'envoi WebSocket: {e}")
    
    return db_notif

def marquer_comme_lue(db: Session, notif_id: UUID, user_id: UUID = None) -> Optional[Notification]:
    """
    Marque une notification comme lue
    
    Args:
        db: Session de base de données
        notif_id: ID de la notification
        user_id: ID de l'utilisateur (pour vérification de propriété)
    
    Returns:
        La notification mise à jour ou None si non trouvée
    """
    query = db.query(Notification).filter(Notification.id == notif_id)
    
    # Si user_id est fourni, vérifier que la notification appartient à cet utilisateur
    if user_id:
        query = query.filter(Notification.user_id == user_id)
    
    notif = query.first()
    if notif:
        notif.lu = True
        db.commit()
        db.refresh(notif)
    
    return notif

def marquer_toutes_comme_lues(db: Session, user_id: UUID, user_type: str) -> int:
    """
    Marque toutes les notifications d'un utilisateur comme lues
    
    Args:
        db: Session de base de données
        user_id: ID de l'utilisateur
        user_type: Type d'utilisateur
    
    Returns:
        Nombre de notifications mises à jour
    """
    notifications_non_lues = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.user_type == user_type,
        Notification.lu == False
    )
    
    count = notifications_non_lues.count()
    notifications_non_lues.update({Notification.lu: True})
    db.commit()
    
    return count

def supprimer_notification(db: Session, notif_id: UUID, user_id: UUID = None) -> bool:
    """
    Supprime une notification
    
    Args:
        db: Session de base de données
        notif_id: ID de la notification
        user_id: ID de l'utilisateur (pour vérification de propriété)
    
    Returns:
        True si supprimée, False sinon
    """
    query = db.query(Notification).filter(Notification.id == notif_id)
    
    if user_id:
        query = query.filter(Notification.user_id == user_id)
    
    notif = query.first()
    if notif:
        db.delete(notif)
        db.commit()
        return True
    
    return False

def supprimer_notifications_lues(db: Session, user_id: UUID, user_type: str) -> int:
    """
    Supprime toutes les notifications lues d'un utilisateur
    
    Args:
        db: Session de base de données
        user_id: ID de l'utilisateur
        user_type: Type d'utilisateur
    
    Returns:
        Nombre de notifications supprimées
    """
    notifications_lues = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.user_type == user_type,
        Notification.lu == True
    )
    
    count = notifications_lues.count()
    notifications_lues.delete()
    db.commit()
    
    return count

# WebSocket endpoint amélioré
async def websocket_endpoint(websocket: WebSocket, user_id: str = None, user_type: str = None):
    """
    Endpoint WebSocket pour les notifications en temps réel
    
    Args:
        websocket: Connexion WebSocket
        user_id: ID de l'utilisateur connecté
        user_type: Type d'utilisateur
    """
    if not user_id or not user_type:
        await websocket.close(code=1008, reason="user_id et user_type requis")
        return

    user_key = f"{user_id}_{user_type}"
    await websocket_manager.connect(websocket, user_key)
    
    try:
        # Envoyer un message de confirmation de connexion
        await websocket.send_text(json.dumps({
            "type": "connection_established",
            "message": "Connexion WebSocket établie pour les notifications"
        }))
        
        while True:
            # Recevoir des messages du client
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                
                # Traiter différents types de messages
                if message.get("type") == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))
                elif message.get("type") == "mark_as_read":
                    # Le client peut marquer des notifications comme lues via WebSocket
                    notification_id = message.get("notification_id")
                    if notification_id:
                        # Ici, vous pourriez ajouter la logique pour marquer comme lu
                        await websocket.send_text(json.dumps({
                            "type": "notification_marked_read",
                            "notification_id": notification_id
                        }))
                        
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Format JSON invalide"
                }))
            
    except WebSocketDisconnect:
        await websocket_manager.disconnect(websocket, user_key)
    except Exception as e:
        print(f"Erreur WebSocket: {e}")
        await websocket_manager.disconnect(websocket, user_key)