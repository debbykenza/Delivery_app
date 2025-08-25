import bcrypt
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
        hashed_pw = bcrypt.hashpw(livreur_data.mot_de_passe.encode("utf-8"), bcrypt.gensalt())
        livreur_dict = livreur_data.dict()
        livreur_dict["mot_de_passe"] = hashed_pw.decode("utf-8")

        livreur = LivreurModel(**livreur_dict)
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
    
    
    
    def authentifier_livreur(db: Session, contact: str, mot_de_passe: str) -> LivreurModel | None:
        livreur = db.query(LivreurModel).filter(LivreurModel.contact == contact).first()

        if not livreur:
            # Email non trouvé ➜ notification "échec"
            notif = NotificationCreate(
                user_id=None,
                user_type="livreur",
                titre="Échec de connexion",
                message=f"Aucun compte n'est associé à ce numéro.",
                type=TypeNotification.error
            )
            creer_notification(db, notif)
            return None

        if not livreur.mot_de_passe or not bcrypt.checkpw(mot_de_passe.encode('utf-8'), livreur.mot_de_passe.encode('utf-8')):
            # Mot de passe incorrect ➜ notification "échec"
            notif = NotificationCreate(
                user_id=livreur.id,
                user_type="livreur",
                titre="Connexion échouée",
                message="Mot de passe incorrect. Veuillez réessayer.",
                type=TypeNotification.warning
            )
            creer_notification(db, notif)
            return None

        #  Connexion réussie ➜ notification "succès"
        notif = NotificationCreate(
            user_id=livreur.id,
            user_type="livreur",
            titre="Connexion réussie",
            message=f"Bonjour {livreur.nom}, vous vous êtes connecté avec succès.",
            type=TypeNotification.info
        )
        creer_notification(db, notif)
        
        #  Notification après authentification réussie
        notif = NotificationCreate(
            user_id=livreur.id,
            user_type="livreur",
            titre="Connexion réussie",
            message=f"Bonjour {livreur.nom}, vous vous êtes connecté avec succès.",
            type=TypeNotification.info
        )
        creer_notification(db, notif)

        return livreur


    def activer_livreur(db: Session, livreur_id: UUID) -> LivreurModel:
        """
        Active un utilisateur en mettant à jour son statut is_active.
        """
        livreur = db.query(LivreurModel).filter(LivreurModel.id == livreur_id).first()
        if not livreur:
            return None

        livreur.est_actif = True
        db.commit()
        db.refresh(livreur)
        
        notif = NotificationCreate(
            user_id=livreur.id,
            user_type="livreur",
            titre="Compte activé",
            message="Votre compte a été activé par l'administrateur",
            type=TypeNotification.success
        )
        creer_notification(db, notif)
        return livreur

    def desactiver_livreur(db: Session, livreur_id: UUID) -> LivreurModel:
        """
        Désactive un livreur en mettant à jour son statut is_active.
        """
        livreur = db.query(LivreurModel).filter(LivreurModel.id == livreur_id).first()
        if not livreur:
            return None

        livreur.est_actif = False
        db.commit()
        db.refresh(livreur)
        
        notif = NotificationCreate(
            user_id=livreur.id,
            user_type="livreur",
            titre="Compte désactivé",
            message="Votre compte a été désactivé. Contactez l'administrateur si besoin.",
            type=TypeNotification.error
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
    
    @staticmethod
    def verifier_contact_existe(db: Session, contact: str) -> bool:
        livreur = db.query(LivreurModel).filter(LivreurModel.contact == contact).first()
        return livreur is not None