from sqlalchemy.orm import Session
from app.models.commande import Commande
from app.models.livreur import Livreur as LivreurModel
from app.models.notification import TypeNotification
from app.schemas.livreur import LivreurCreate, LivreurUpdate, StatutLivreurUpdate
from uuid import UUID

from app.schemas.notification import NotificationCreate
from app.services.notification import creer_notification


class LivreurService:
    @staticmethod
    def creer_livreur(db: Session, livreur_data: LivreurCreate) -> LivreurModel:
        livreur = LivreurModel(**livreur_data.dict())
        db.add(livreur)
        db.commit()
        db.refresh(livreur)
        
        notif = NotificationCreate(
            user_id=livreur.id,
            user_type="livreur",
            titre="Compte livreur créé",
            message="Un nouveau compte livreur a été enregistré.",
            type=TypeNotification.success
        )
        creer_notification(db, notif)
        return livreur

    @staticmethod
    def obtenir_livreur(db: Session, livreur_id: UUID):
        return db.query(LivreurModel).filter(LivreurModel.id == livreur_id).first()

    @staticmethod
    def mettre_a_jour_statut(db: Session, livreur_id: UUID, update_data: StatutLivreurUpdate):
        livreur = db.query(LivreurModel).filter(LivreurModel.id == livreur_id).first()
        if not livreur:
            return None

        livreur.statut = update_data.nouveau_statut
        db.commit()
        db.refresh(livreur)
        
        notif = NotificationCreate(
            user_id=livreur.id,
            user_type="livreur",
            titre="Statut mis à jour",
            message=f"Votre statut est désormais : {livreur.statut}",
            type=TypeNotification.info
        )
        creer_notification(db, notif)
        return livreur

    @staticmethod
    def lister_livreurs(db: Session):
        return db.query(LivreurModel).all()




    @staticmethod
    def modifier_livreur(db: Session, livreur_id: UUID, update_data: LivreurUpdate) -> LivreurModel:
        livreur = db.query(LivreurModel).filter(LivreurModel.id == livreur_id).first()
        if not livreur:
            return None
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(livreur, key, value)
        db.commit()
        db.refresh(livreur)
        
        notif = NotificationCreate(
            user_id=livreur.id,
            user_type="livreur",
            titre="Profil mis à jour",
            message="Vos informations personnelles ont été modifiées.",
            type=TypeNotification.info
        )
        creer_notification(db, notif)
        return livreur

    
    @staticmethod
    def supprimer_livreur(db: Session, livreur_id: UUID):
        livreur = db.query(LivreurModel).filter(LivreurModel.id == livreur_id).first()
        if not livreur:
            return False
        
        notif = NotificationCreate(
            user_id=livreur.id,
            user_type="livreur",
            titre="Compte supprimé",
            message="Votre compte a été supprimé du système.",
            type=TypeNotification.warning
        )
        creer_notification(db, notif)
        db.delete(livreur)
        db.commit()
        return True

    @staticmethod
    def voir_details_commande(db: Session, commande_id: UUID):
        commande = db.query(Commande).filter(Commande.id == commande_id).first()
        return commande
    
    