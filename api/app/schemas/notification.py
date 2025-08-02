# from datetime import datetime
# from enum import Enum
# from typing import Optional
# from uuid import UUID
# from pydantic import BaseModel
# from app.models.livreur import Livreur

# class TypeNotification(str, Enum):
#     info = "info"
#     warning = "warning"
#     error = "error"
#     success = "success"

# class NotificationBase(BaseModel):
#     user_id: UUID
#     user_type: str
#     titre: str
#     message: str
#     type: TypeNotification = TypeNotification.info

# class NotificationCreate(NotificationBase):
#     pass

# class NotificationUpdate(BaseModel):
#     lu: bool

# class NotificationRead(NotificationBase):
#     id: UUID
#     lu: bool
#     date_envoi: datetime

#     class Config:
#         orm_mode = True
#         json_schema_extra = {
#             "example": {
#                 "id": "d1f4c1c1-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
#                 "user_id": "abf4c1c1-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
#                 "user_type": "client",
#                 "titre": "Nouvelle commande",
#                 "message": "Votre commande a été validée.",
#                 "type": "success",
#                 "lu": False,
#                 "date_envoi": datetime.utcnow().isoformat()
#             }
#         }

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field

class TypeNotification(str, Enum):
    info = "info"
    warning = "warning"
    error = "error"
    success = "success"

class NotificationBase(BaseModel):
    user_id: UUID
    user_type: str = Field(..., description="Type d'utilisateur: client, marchand, livreur, admin")
    titre: str = Field(..., min_length=1, max_length=200, description="Titre de la notification")
    message: str = Field(..., min_length=1, max_length=1000, description="Message de la notification")
    type: TypeNotification = Field(default=TypeNotification.info, description="Type de notification")

class NotificationCreate(NotificationBase):
    """Schéma pour créer une notification"""
    pass

class NotificationUpdate(BaseModel):
    """Schéma pour mettre à jour une notification"""
    lu: bool
    
class NotificationRead(NotificationBase):
    """Schéma pour lire une notification"""
    id: UUID
    lu: bool = Field(description="Statut de lecture de la notification")
    date_envoi: datetime = Field(description="Date et heure d'envoi de la notification")

    class Config:
        from_attributes = True  # Pour Pydantic v2, remplace orm_mode = True
        json_schema_extra = {
            "example": {
                "id": "d1f4c1c1-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "user_id": "abf4c1c1-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "user_type": "client",
                "titre": "Nouvelle commande",
                "message": "Votre commande a été validée.",
                "type": "success",
                "lu": False,
                "date_envoi": "2024-07-19T10:30:00"
            }
        }

class NotificationStats(BaseModel):
    """Schéma pour les statistiques des notifications"""
    user_id: str
    user_type: str
    total: int = Field(description="Nombre total de notifications")
    non_lues: int = Field(description="Nombre de notifications non lues")
    lues: int = Field(description="Nombre de notifications lues")
    recentes_24h: int = Field(description="Notifications des dernières 24h")
    par_type: Dict[str, int] = Field(description="Répartition par type de notification")

class NotificationCount(BaseModel):
    """Schéma pour le comptage des notifications"""
    user_id: str
    non_lues: int = Field(description="Nombre de notifications non lues")

class NotificationResponse(BaseModel):
    """Schéma pour les réponses d'actions sur les notifications"""
    message: str
    count: Optional[int] = None
    user_id: str

class WebSocketMessage(BaseModel):
    """Schéma pour les messages WebSocket"""
    type: str = Field(description="Type de message WebSocket")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Données du message")
    notification_id: Optional[str] = Field(default=None, description="ID de la notification concernée")

class NotificationFilter(BaseModel):
    """Schéma pour les filtres de notifications"""
    user_id: UUID
    user_type: str
    non_lues: Optional[bool] = False
    type_notification: Optional[TypeNotification] = None
    limite: Optional[int] = Field(default=50, ge=1, le=100)
    depuis_jours: Optional[int] = Field(default=None, ge=1, le=365)