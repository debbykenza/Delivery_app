from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.schemas.notification import NotificationCreate, NotificationRead, NotificationUpdate
from app.services.notification import lire_notifications as service_lire_notifications, creer_notification, marquer_comme_lue
from app.core.database import get_db

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/", response_model=List[NotificationRead])
def lire_notifications(
    user_id: UUID,
    user_type: str,
    non_lues: bool = False,
    db: Session = Depends(get_db)
):
    return service_lire_notifications(db, user_id=user_id, user_type=user_type, seulement_non_lues=non_lues)

@router.post("/", response_model=NotificationRead, status_code=status.HTTP_201_CREATED)
def ajouter_notification(notif: NotificationCreate, db: Session = Depends(get_db)):
    return creer_notification(db, notif)

@router.patch("/{notif_id}/lue", response_model=NotificationRead)
def marquer_notification_comme_lue(notif_id: UUID, db: Session = Depends(get_db)):
    notif = marquer_comme_lue(db, notif_id)
    if not notif:
        raise HTTPException(status_code=404, detail="Notification non trouvée")
    return notif
