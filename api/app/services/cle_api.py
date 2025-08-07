from typing import Optional
from fastapi import HTTPException 
from app.models.cle_api import CleAPI
from app.models.marchand import Marchand
from app.models.notification import TypeNotification
from app.schemas.cle_api import CleAPICreate, CleAPIParMarchand, CleAPIResponse
from sqlalchemy.orm import Session
from uuid import UUID
import secrets
from app.models.utilisateur import Utilisateur
from app.schemas.notification import NotificationCreate
from app.services.notification import creer_notification

# def creer_cle(db: Session, data: CleAPICreate) -> CleAPI:
#     cle = secrets.token_hex(32)
#     cle_api = CleAPI(
#         cle=cle,
#         nom=data.nom,
#         utilisateur_id=data.utilisateur_id,
#         marchand_id=data.marchand_id,
#     )
#     db.add(cle_api)
#     db.commit()
#     db.refresh(cle_api)
    
#      # Notification de création
#     notif = NotificationCreate(
#         user_id=data.utilisateur_id,
#         user_type="utilisateur",
#         titre="Nouvelle clé API créée",
#         message=f"La clé API « {data.nom} » a été générée.",
#         type=TypeNotification.success
#     )
#     creer_notification(db, notif)
    
#      # ✅ Récupérer le nom du marchand
#     marchand = db.query(Marchand).filter(Marchand.id == data.marchand_id).first()

#     return CleAPIResponse(
#         id=cle_api.id,
#         nom=cle_api.nom,
#         cle=cle_api.cle,
#         utilisateur_id=cle_api.utilisateur_id,
#         marchand_nom=marchand.nom if marchand else None,
#         est_active=cle_api.est_active,
#         date_creation=cle_api.date_creation
#     )
#     # return cle_api

# def recuperer_cles_par_utilisateur(db: Session, utilisateur_id: UUID):
#     return db.query(CleAPI).filter(CleAPI.utilisateur_id == utilisateur_id).all()

def creer_cle(db: Session, data: CleAPICreate) -> CleAPIResponse:
    """Créer une nouvelle clé API"""
    cle = secrets.token_hex(32)
    cle_api = CleAPI(
        cle=cle,
        nom=data.nom,
        utilisateur_id=data.utilisateur_id,
        marchand_id=data.marchand_id,
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
    
    # Récupérer le nom du marchand
    marchand = db.query(Marchand).filter(Marchand.id == data.marchand_id).first()

    # Retourner la réponse formatée
    return CleAPIResponse(
        id=cle_api.id,
        nom=cle_api.nom,
        cle=cle_api.cle,
        utilisateur_id=cle_api.utilisateur_id,
        marchand_nom=marchand.nom if marchand else None,
        est_active=cle_api.est_active,
        date_creation=cle_api.date_creation
    )

def recuperer_toutes_les_cles(db: Session) -> list[CleAPIResponse]:
    """Retourne toutes les clés API de la base de données"""
    cles = db.query(CleAPI).all()
    result = []

    for cle in cles:
        # Récupérer le nom du marchand
        marchand = db.query(Marchand).filter(Marchand.id == cle.marchand_id).first()

        result.append(CleAPIResponse(
            id=cle.id,
            nom=cle.nom,
            cle=cle.cle,
            utilisateur_id=cle.utilisateur_id,
            marchand_nom=marchand.nom if marchand else None,
            est_active=cle.est_active,
            date_creation=cle.date_creation
        ))
    
    return result


def recuperer_cles_par_utilisateur(db: Session, utilisateur_id: UUID) -> list[CleAPIResponse]:
    """Récupérer toutes les clés API d'un utilisateur avec les noms des marchands"""
    cles = db.query(CleAPI).filter(CleAPI.utilisateur_id == utilisateur_id).all()
    
    result = []
    for cle in cles:
        # Récupérer le nom du marchand
        marchand = db.query(Marchand).filter(Marchand.id == cle.marchand_id).first()
        
        result.append(CleAPIResponse(
            id=cle.id,
            nom=cle.nom,
            cle=cle.cle,
            utilisateur_id=cle.utilisateur_id,
            marchand_nom=marchand.nom if marchand else None,
            est_active=cle.est_active,
            date_creation=cle.date_creation
        ))
    
    return result

def recuperer_cles_par_marchand(db: Session, marchand_id: UUID):
    return db.query(CleAPI).filter(CleAPI.marchand_id == marchand_id).all()


def obtenir_cle_par_marchand(
    db: Session, 
    marchand_id: UUID,
    utilisateur_id: UUID
) -> CleAPIParMarchand:
    """
    Récupère la clé API associée à un marchand spécifique
    Vérifie que l'utilisateur a bien accès à ce marchand
    """
    # Vérifier d'abord que l'utilisateur possède ce marchand
    marchand = db.query(Marchand).filter(
        Marchand.id == marchand_id,
        Marchand.utilisateur_id == utilisateur_id
    ).first()

    if not marchand:
        raise HTTPException(
            status_code=404,
            detail="Marchand non trouvé ou non autorisé"
        )

    cle = db.query(CleAPI).filter(
        CleAPI.marchand_id == marchand_id,
        CleAPI.est_active == True
    ).first()

    if not cle:
        raise HTTPException(
            status_code=404,
            detail="Aucune clé API active trouvée pour ce marchand"
        )

    return cle

# def supprimer_cle(db: Session, cle_id: UUID):
#     cle = db.query(CleAPI).filter(CleAPI.id == cle_id).first()
#     if not cle:
#         raise HTTPException(status_code=404, detail="Clé introuvable")

#     # ✅ Notification avec les bons champs
#     notif = NotificationCreate(
#         user_id=cle.utilisateur_id,
#         user_type="utilisateur",
#         titre="Clé API supprimée",
#         message=f"La clé API « {cle.nom} » a été supprimée.",
#         type=TypeNotification.warning
#     )
#     creer_notification(db, notif)

#     db.delete(cle)
#     db.commit()
#     return {"message": "Clé supprimée avec succès"}


# def revoquer_cle(db: Session, cle_id: UUID):
#     cle = db.query(CleAPI).filter(CleAPI.id == cle_id).first()
#     if not cle:
#         raise HTTPException(status_code=404, detail="Clé introuvable")
#     cle.est_active = False
#     db.commit()
#     db.refresh(cle)
    
#     notif = NotificationCreate(
#         user_id=cle.utilisateur_id,
#         user_type="utilisateur",
#         titre="Clé API révoquée",
#         message=f"La clé API « {cle.nom} » a été révoquée.",
#         type=TypeNotification.error
#     )
#     creer_notification(db, notif)
#     return cle

def revoquer_cle(db: Session, cle_id: UUID, utilisateur_id: UUID):
    cle = db.query(CleAPI).filter(CleAPI.id == cle_id).first()
    if not cle:
        raise HTTPException(status_code=404, detail="Clé introuvable")
    
    # Vérifier que l'utilisateur est propriétaire de la clé
    if cle.utilisateur_id != utilisateur_id:
        raise HTTPException(status_code=403, detail="Non autorisé")
    
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

# def nommer_cle(db: Session, cle_id: UUID, nouveau_nom: str):
#     cle = db.query(CleAPI).filter(CleAPI.id == cle_id).first()
#     if not cle:
#         raise HTTPException(status_code=404, detail="Clé introuvable")
#     cle.nom = nouveau_nom
#     db.commit()
#     db.refresh(cle)
    
#     notif = NotificationCreate(
#         user_id=cle.utilisateur_id,
#         user_type="utilisateur",
#         titre="Nom de clé modifié",
#         message=f"La clé API a été renommée en « {nouveau_nom} ».",
#         type=TypeNotification.info
#     )
#     creer_notification(db, notif)
#     return cle

# def regenerer_cle(db: Session, cle_id: UUID):
#     cle = db.query(CleAPI).filter(CleAPI.id == cle_id).first()
#     if not cle:
#         raise HTTPException(status_code=404, detail="Clé introuvable")
#     cle.cle = secrets.token_hex(32)
#     cle.est_active = True
#     db.commit()
#     db.refresh(cle)
    
#     notif = NotificationCreate(
#         user_id=cle.utilisateur_id,
#         user_type="utilisateur",
#         titre="Clé API régénérée",
#         message=f"La clé API « {cle.nom} » a été régénérée et réactivée.",
#         type=TypeNotification.info
#     )
#     creer_notification(db, notif)
#     return cle

def consulter_statistiques(db: Session, utilisateur_id: UUID):
    total = db.query(CleAPI).filter(CleAPI.utilisateur_id == utilisateur_id).count()
    actives = db.query(CleAPI).filter(CleAPI.utilisateur_id == utilisateur_id, CleAPI.est_active == True).count()
    inactives = total - actives
    return {
        "total_cles": total,
        "cles_actives": actives,
        "cles_revoquees": inactives
    }

def supprimer_cle(db: Session, cle_id: UUID, utilisateur_id: UUID):
    cle = db.query(CleAPI).filter(
        CleAPI.id == cle_id,
        CleAPI.utilisateur_id == utilisateur_id
    ).first()
    
    if not cle:
        raise HTTPException(status_code=404, detail="Clé introuvable ou non autorisée")

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

def nommer_cle(db: Session, cle_id: UUID, nouveau_nom: str, utilisateur_id: UUID):
    cle = db.query(CleAPI).filter(
        CleAPI.id == cle_id,
        CleAPI.utilisateur_id == utilisateur_id
    ).first()
    
    if not cle:
        raise HTTPException(status_code=404, detail="Clé introuvable ou non autorisée")
    
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

def modifier_cle(
    db: Session, 
    cle_id: UUID, 
    utilisateur_id: UUID,
    nouveau_nom: Optional[str] = None,
    nouveau_marchand_id: Optional[UUID] = None
) -> CleAPI:
    """
    Modifie une clé API existante.
    Permet de changer le nom et/ou le marchand associé.
    """
    cle = db.query(CleAPI).filter(
        CleAPI.id == cle_id,
        CleAPI.utilisateur_id == utilisateur_id
    ).first()
    
    if not cle:
        raise HTTPException(status_code=404, detail="Clé introuvable ou non autorisée")
    
    modifications = []
    
    if nouveau_nom is not None:
        cle.nom = nouveau_nom
        modifications.append(f"nom → {nouveau_nom}")
    
    if nouveau_marchand_id is not None:
        # Vérifier que le nouveau marchand existe
        marchand = db.query(Marchand).filter(Marchand.id == nouveau_marchand_id).first()
        if not marchand:
            raise HTTPException(status_code=404, detail="Marchand introuvable")
        
        cle.marchand_id = nouveau_marchand_id
        modifications.append(f"marchand → {marchand.nom}")
    
    if not modifications:
        raise HTTPException(status_code=400, detail="Aucune modification fournie")
    
    db.commit()
    db.refresh(cle)
    
    # Notification
    notif = NotificationCreate(
        user_id=utilisateur_id,
        user_type="utilisateur",
        titre="Clé API modifiée",
        message=f"La clé API a été modifiée ({', '.join(modifications)}).",
        type=TypeNotification.info
    )
    creer_notification(db, notif)
    
    return cle

def regenerer_cle(db: Session, cle_id: UUID, utilisateur_id: UUID):
    cle = db.query(CleAPI).filter(
        CleAPI.id == cle_id,
        CleAPI.utilisateur_id == utilisateur_id
    ).first()
    
    if not cle:
        raise HTTPException(status_code=404, detail="Clé introuvable ou non autorisée")
    
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