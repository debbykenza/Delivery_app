from fastapi import HTTPException 
from app.models.cle_api import CleAPI
from app.models.notification import TypeNotification
from app.schemas.cle_api import CleAPICreate
from sqlalchemy.orm import Session
from uuid import UUID
import secrets
from app.models.utilisateur import Utilisateur
from app.schemas.notification import NotificationCreate
from app.services.notification import creer_notification

def creer_cle(db: Session, data: CleAPICreate) -> CleAPI:
    cle = secrets.token_hex(32)
    cle_api = CleAPI(
        cle=cle,
        nom=data.nom,
        utilisateur_id=data.utilisateur_id
    )
    db.add(cle_api)
    db.commit()
    db.refresh(cle_api)
    
     # Notification de création
    notif = NotificationCreate(
        user_id=data.utilisateur_id,
        user_type="utilisateur",
        titre="Nouvelle clé API créée",
        message=f"La clé API « {data.nom} » a été générée.",
        type=TypeNotification.success
    )
    creer_notification(db, notif)
    return cle_api

def recuperer_cles_par_utilisateur(db: Session, utilisateur_id: UUID):
    return db.query(CleAPI).filter(CleAPI.utilisateur_id == utilisateur_id).all()

def supprimer_cle(db: Session, cle_id: UUID):
    cle = db.query(CleAPI).filter(CleAPI.id == cle_id).first()
    if not cle:
        raise HTTPException(status_code=404, detail="Clé introuvable")

    # ✅ Notification avec les bons champs
    notif = NotificationCreate(
        user_id=cle.utilisateur_id,
        user_type="utilisateur",
        titre="Clé API supprimée",
        message=f"La clé API « {cle.nom} » a été supprimée.",
        type=TypeNotification.warning
    )
    creer_notification(db, notif)

    db.delete(cle)
    db.commit()
    return {"message": "Clé supprimée avec succès"}


def revoquer_cle(db: Session, cle_id: UUID):
    cle = db.query(CleAPI).filter(CleAPI.id == cle_id).first()
    if not cle:
        raise HTTPException(status_code=404, detail="Clé introuvable")
    cle.est_active = False
    db.commit()
    db.refresh(cle)
    
    notif = NotificationCreate(
        user_id=cle.utilisateur_id,
        user_type="utilisateur",
        titre="Clé API révoquée",
        message=f"La clé API « {cle.nom} » a été révoquée.",
        type=TypeNotification.error
    )
    creer_notification(db, notif)
    return cle

def nommer_cle(db: Session, cle_id: UUID, nouveau_nom: str):
    cle = db.query(CleAPI).filter(CleAPI.id == cle_id).first()
    if not cle:
        raise HTTPException(status_code=404, detail="Clé introuvable")
    cle.nom = nouveau_nom
    db.commit()
    db.refresh(cle)
    
    notif = NotificationCreate(
        user_id=cle.utilisateur_id,
        user_type="utilisateur",
        titre="Nom de clé modifié",
        message=f"La clé API a été renommée en « {nouveau_nom} ».",
        type=TypeNotification.info
    )
    creer_notification(db, notif)
    return cle

def regenerer_cle(db: Session, cle_id: UUID):
    cle = db.query(CleAPI).filter(CleAPI.id == cle_id).first()
    if not cle:
        raise HTTPException(status_code=404, detail="Clé introuvable")
    cle.cle = secrets.token_hex(32)
    cle.est_active = True
    db.commit()
    db.refresh(cle)
    
    notif = NotificationCreate(
        user_id=cle.utilisateur_id,
        user_type="utilisateur",
        titre="Clé API régénérée",
        message=f"La clé API « {cle.nom} » a été régénérée et réactivée.",
        type=TypeNotification.info
    )
    creer_notification(db, notif)
    return cle

def consulter_statistiques(db: Session, utilisateur_id: UUID):
    total = db.query(CleAPI).filter(CleAPI.utilisateur_id == utilisateur_id).count()
    actives = db.query(CleAPI).filter(CleAPI.utilisateur_id == utilisateur_id, CleAPI.est_active == True).count()
    inactives = total - actives
    return {
        "total_cles": total,
        "cles_actives": actives,
        "cles_revoquees": inactives
    }
