from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.avis import Avis
from app.models.livreur import Livreur
from app.models.notification import TypeNotification
from app.schemas.avis import AvisCreate
from app.schemas.notification import NotificationCreate
from app.services.notification import creer_notification

class ServiceAvis:
    @staticmethod
    def creer_avis(db: Session, avis_data: AvisCreate) -> Avis:
        # nouvel_avis = Avis(
        #     livreur_id=avis_data.livreur_id,
        #     livraison_id=avis_data.livraison_id,
        #     client_id=avis_data.client_id,
        #     commentaire=avis_data.commentaire,
        #     note=avis_data.note,
        #     date_avis=datetime.utcnow()
        # )
        nouvel_avis = Avis(
            livreur_id=avis_data.livreur_id,
            livraison_id=avis_data.livraison_id,
            client_id=avis_data.client_id,
            commentaire=avis_data.commentaire,
            note=avis_data.note
        )
        db.add(nouvel_avis)
        db.commit()
        db.refresh(nouvel_avis)
        
         # Création de la notification pour le livreur
        notif = NotificationCreate(
            user_id=avis_data.livreur_id,
            user_type="livreur",
            titre="Nouvel avis reçu",
            message=f"Vous avez reçu un nouvel avis avec la note {avis_data.note}.",
            type=TypeNotification.info
        )
        creer_notification(db, notif)

        # 🔔 Notification pour le client
        notif_client = NotificationCreate(
            user_id=avis_data.client_id,
            user_type="client",
            titre="Avis enregistré",
            message="Votre avis a été bien enregistré. Merci pour votre retour !",
            type=TypeNotification.success
        )
        creer_notification(db, notif_client)
        
        return nouvel_avis

    @staticmethod
    def supprimer_avis(db: Session, avis_id: UUID) -> bool:
        """
        Supprime un avis à partir de son identifiant.
        """
        avis = db.query(Avis).filter(Avis.id == avis_id).first()
        if avis:
            
            # ✅ Récupération des IDs
            livreur_id = avis.livreur_id
            client_id = avis.client_id

            
            db.delete(avis)
            db.commit()
            
            # 🔔 Notification au livreur
            notif_livreur = NotificationCreate(
                user_id=livreur_id,
                user_type="livreur",
                titre="Avis supprimé",
                message="Un des avis que vous avez reçus a été supprimé.",
                type=TypeNotification.warning
            )
            creer_notification(db, notif_livreur)

            # 🔔 Notification au client
            notif_client = NotificationCreate(
                user_id=client_id,
                user_type="client",
                titre="Avis supprimé",
                message="Votre avis a été supprimé de notre système.",
                type=TypeNotification.info
            )
            creer_notification(db, notif_client)
            return True
        return False

    @staticmethod
    def lister_avis(db: Session):
        """
        Récupère tous les avis présents dans la base de données.
        """
        return db.query(Avis).all()

    @staticmethod
    def lister_avis_par_livreur(db: Session, livreur_id: UUID):
        """
        Récupère les avis donnés à un livreur spécifique.
        """
        return db.query(Avis).filter(Avis.livreur_id == livreur_id).all()