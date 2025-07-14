from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.models.notification import Notification, TypeNotification
from app.schemas.notification import NotificationCreate

# def lire_notifications(db: Session, user_id: UUID, user_type: str, seulement_non_lues: bool = False) -> List[Notification]:
#     query = db.query(Notification).filter(
#         Notification.user_id == user_id,
#         Notification.user_type == user_type
#     )
#     if seulement_non_lues:
#         query = query.filter(Notification.lu == False)
#     return query.order_by(Notification.date_envoi.desc()).all()

def lire_notifications(db: Session, user_id: UUID, user_type: str, seulement_non_lues: bool = False) -> List[Notification]:
    query = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.user_type == user_type
    )

    # ➤ Nouveau filtre selon la valeur de seulement_non_lues
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
